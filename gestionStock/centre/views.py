from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView,View
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Produit,Vente,Client,Employe, Absence, Avance
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import SaleForm,AbsenceForm
from django.db.models import Sum,Count
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from .serializers import ProduitVenteSerializer,TopCustomerSerializer,AbsenceChartSerializer

def afficher_ventes(request):
    ventes=Vente.objects.all()
    return render(request,'centre/afficher_ventes.html',{'ventes':ventes})


def update_stock_after_sale(vente_id):
    vente = get_object_or_404(Vente, pk=vente_id)

    # Vérifier si le produit a suffisamment de stock
    if vente.produit.qteStock >= vente.qteVente:
        # Mettre à jour la quantité du produit
        vente.produit.qteStock -= vente.qteVente
        vente.produit.save()
    else:
        return HttpResponseBadRequest("Quantité de produit insuffisante en stock.")

def record_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.prix_total = sale.qteVente * sale.prixUniVente
            sale.save()

            # Appeler la fonction pour mettre à jour le stock
            update_stock_after_sale(sale.pk)

            return render(request, 'centre/record_sale.html', {'form': form, 'prix_total': sale.prix_total})
    else:
        form = SaleForm()

    return render(request, 'centre/record_sale.html', {'form': form})



def vente(request):
  vente_instance = Vente()
    # Calculer le montant total des ventes
  montant_total_ventes = vente_instance.montant_total_ventes()

  return render(request, 'centre/afficher_ventes.html', {'montant_total_ventes': montant_total_ventes})
#charts Vente et Client
def chart_view(request):
    return render(request, 'centre/dashboard.html')

class ProduitVenteChart(APIView):
    def get(self, request, format=None):
        data = Vente.objects.values('produit__Designation').annotate(total_ventes=Sum('qteVente'))
        serializer = ProduitVenteSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    

class TopCustomerChart(APIView):
    def get(self, request, format=None):
       
        end_date = datetime.date.today()
        start_date = end_date - relativedelta(months=12)

        data = (
            Vente.objects
            .filter(date__range=(start_date, end_date))
            .values('client__nomPrenomC')
            .annotate(total_purchases=Sum('qteVente'))
            .order_by('-total_purchases')[:10]  # Get top 10 customers
        )

        serializer = TopCustomerSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def chart_view2(request):
    return render(request, 'centre/clientchart.html')

#EmployeManagement
class EmployeManagementView(View):
   

    def get(self, request):
        # Partie 1 - Overview
        total_employees = Employe.objects.count()
        current_date = datetime.date.today()
        present_percentage = 100 * Absence.objects.filter(dateAbsence=current_date).values('emp').annotate(count=Count('emp')).count() / total_employees
        total_absences = Absence.objects.filter(dateAbsence=current_date).count()

        # Partie 2 - Chart d'absence pour l'année
        absences_data = Absence.objects.filter(dateAbsence__year=current_date.year).values('emp__nomPrenomE').annotate(total_absences=Count('emp'))

        return render(request,'centre/employe-management.html',{
            'total_employees': total_employees,
            'present_percentage': present_percentage,
            'total_absences': total_absences,
            'absences_data': absences_data,
        })
    

def absence_create(request):
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employe-management')  # Redirige vers la liste des absences
    else:
        form = AbsenceForm()

    return render(request, 'centre/absence.html', {'form': form})
class AbsenceChartAPIView(APIView):
    def get(self, request, format=None):
        absences_data = Absence.objects.values('emp__nomPrenomE').annotate(total_absences=Count('emp__absence__dateAbsence')).order_by('emp__nomPrenomE')
        serializer = AbsenceChartSerializer(absences_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
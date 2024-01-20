from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView,View
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Produit,Vente,Client,Employe, Absence, Avance,CreditPayment,TransfertRecu,Reglement
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import SaleForm,AbsenceForm,AvanceForm,ReglementForm
from django.db.models import Sum,Count
import datetime
from datetime import date,timedelta,datetime
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
    template_name = 'centre/record_sale.html'

    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.prix_total = sale.qteVente * sale.prixUniVente
            sale.save()

            # Appeler la fonction pour mettre à jour le stock
            update_stock_after_sale(sale.pk)
            if not sale.PayEnt:
                # Si le paiement n'est pas entièrement effectué, traiter le montant payé
                montant_paye = form.cleaned_data.get('montant_paye')
                CreditPayment.objects.create(
                    date=sale.date,
                    client=sale.client,
                    amount_paid=montant_paye,
                    vente=sale
                )
             
                # Mise à jour automatique du crédit client (ajoute automatiquement le reste à payer au crédit client)
                reste_a_payer = sale.prix_total - montant_paye
                sale.client.credit += reste_a_payer
                sale.client.save()
            if  sale.PayEnt:    
                sale.montant_paye=sale.prix_total
                sale.save()
            return redirect('afficher_vente')
    form = SaleForm()

    return render(request, 'centre/record_sale.html', {'form': form})




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
       
        end_date = date.today()
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
        current_date = date.today()
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
    template_name = 'centre/absence.html'

    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employe-management')
    else:
        form = AbsenceForm()

    return render(request, 'centre/absence.html', {'form': form})

class AbsenceChartAPIView(APIView):
    def get(self, request, format=None):
        absences_data = Absence.objects.values('emp__nomPrenomE').annotate(total_absences=Count('emp__absence__dateAbsence')).order_by('emp__nomPrenomE')
        serializer = AbsenceChartSerializer(absences_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 


def paiement(request):
    template_name = 'centre/paiement.html'

    avances = Avance.objects.filter(dateAvance__month__gte=1, dateAvance__month__lte=12)

    if request.method == 'POST':
        form = AvanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('paiement')
    else:
        form = AvanceForm()

    return render(request, template_name, {'avances': avances, 'form': form})



def liste_employes(request):
    template_name = 'centre/liste_employes.html'

    employes = Employe.objects.all()

    return render(request, template_name, {'employes': employes})



# LISTES EMPLOYE AVEC SALAIRE 
def liste_employes(request):
    template_name = 'centre/liste_employes.html'

    employes = Employe.objects.all()

    if request.method == 'POST':
        # Calculer les salaires à la fin du mois
        for employe in employes:
            salaire_jour = employe.salaireJour

            # Nombre total de jours dans le mois
            dernier_jour_mois = datetime.now().replace(day=1, month=datetime.now().month + 1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
            nombre_jours_mois = dernier_jour_mois.day

            # Nombre de jours d'absence du mois courant
            absences_mois = Absence.objects.filter(emp=employe, dateAbsence__month=datetime.now().month).count()

            # Montant total des demandes d'avance du mois courant
            avances_mois = Avance.objects.filter(employe=employe, dateAvance__month=datetime.now().month).aggregate(Sum('montantAvance'))['montantAvance__sum'] or 0

            # Calcul du salaire à la fin du mois
            salaire_fin_mois = salaire_jour * (nombre_jours_mois - absences_mois) - avances_mois

            # Mettre à jour le salaire à la fin du mois dans l'objet Employe
            employe.salaireFinMois = salaire_fin_mois
            employe.save()

    return render(request, template_name, {'employes': employes})



def list_transferts_recu(request):
    transferts_recu = TransfertRecu.objects.all()
    return render(request, 'centre/list_transferts_recu.html', {'transferts_recu': transferts_recu})




def calculate_total_and_benefit(request):
    total_ventes = Vente.objects.aggregate(Sum('prix_total'))['prix_total__sum'] or 0
    total_transferts_recu = TransfertRecu.objects.aggregate(Sum('cost'))['cost__sum'] or 0

    benefit = total_ventes - total_transferts_recu

    context = {
        'total_ventes': total_ventes,
        'total_transferts_recu': total_transferts_recu,
        'benefit': benefit,
    }

    return render(request, 'centre/analyse.html', context)

def get_credit_amount(client_id):
    credit_payments = CreditPayment.objects.filter(client_id=client_id)
    total_credit = sum(payment.amount_paid for payment in credit_payments)
    return total_credit



def update_credit(client_id):
    credit_amount = get_credit_amount(client_id)
    return JsonResponse({'credit_amount': credit_amount})

def add_reglement(request):
    form = ReglementForm()

    # Handle form submission
    if request.method == 'POST':
        form = ReglementForm(request.POST)
        if form.is_valid():
            reglement = form.save()

            # Update credit for the selected client
            update_credit(reglement.client.CodeC)

            return redirect('add_reglement')  # Redirect to clear the form

    # Pass the initial credit amount to the template
    client_id = request.POST.get('client', None)
    initial_credit = get_credit_amount(client_id)
    
    return render(request, 'centre/add_reglement.html', {'form': form, 'initial_credit': initial_credit})

def get_client_credit(request):
    client_id = request.GET.get('client_id')
    credit_amount = get_credit_amount(client_id)
    return JsonResponse({'credit_amount': credit_amount})
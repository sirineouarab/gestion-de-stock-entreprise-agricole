from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView,View
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Produit,Vente,Client
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import SaleForm
from django.db.models import Sum
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

from django.http import JsonResponse
from .serializers import ProduitVenteSerializer,TopCustomerSerializer

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

def chart_view(request):
    return render(request, 'centre/dashboard.html')

class ProduitVenteChart(APIView):
    def get(self, request, format=None):
        data = Vente.objects.values('produit__Designation').annotate(total_ventes=Sum('qteVente'))
        serializer = ProduitVenteSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    

class TopCustomerChart(APIView):
    def get(self, request, format=None):
        # Adjust the time range as needed based on the `date_achat` field
        # This example assumes you want data for the last 12 months
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

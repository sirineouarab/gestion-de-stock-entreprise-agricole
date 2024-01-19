from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView,View
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Produit,Vente
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import SaleForm
from django.db.models import Sum,Count
import datetime
from datetime import date,timedelta,datetime
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
# Create your views here.


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
    template_name = 'centre2/record_sale.html'

    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.prix_total = sale.qteVente * sale.prixUniVente
            sale.save()

            # Appeler la fonction pour mettre à jour le stock
            update_stock_after_sale(sale.pk)
            sale.client.save()
            return redirect('record_sale')
    form = SaleForm()

    return render(request, 'centre2/record_sale.html', {'form': form})

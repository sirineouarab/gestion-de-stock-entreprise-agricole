from django.http import HttpResponseBadRequest

from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Produit,Vente
from .forms import SaleForm
import datetime


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

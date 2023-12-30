
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Produit
from .forms import SaleForm
import datetime
def record_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            product=sale.produit
            sale.prixUniVente=product.prixUniVente
            sale.prix_total = sale.qteVente * sale.prixUniVentecd 
            sale.save()
            return render(request, 'centre/record_sale.html', {'form': form})
    else:  
        form = SaleForm()
    
    return render(request, 'centre/record_sale.html', {'form': form})

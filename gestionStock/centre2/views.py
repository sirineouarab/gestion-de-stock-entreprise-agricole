from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView,View
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Produit,Vente,Client,Employe, Absence, Avance,CreditPayment,TransfertRecu,Reglement

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

def afficher_ventes(request):
    ventes=Vente.objects.all()
    return render(request,'centre2/afficher_ventes.html',{'ventes':ventes})



def record_sale(request):
    template_name = 'centre2/record_sale.html'

    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.prix_total = sale.qteVente * sale.prixUniVente
            

            # Appeler la fonction pour mettre à jour le stock
          
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
            # Vérifier si le produit a suffisamment de stock
            if sale.produit.qteStock >= sale.qteVente:
       
        # Mettre à jour la quantité du produit
                 sale.produit.qteStock -=  sale.qteVente
                 sale.produit.save()
            else:
               return HttpResponseBadRequest("Quantité de produit insuffisante en stock.")
 
            return redirect('afficher_vente2')
    form = SaleForm()

    return render(request, 'centre2/record_sale.html', {'form': form})
#tables 

from django.shortcuts import render
from magasin.models import Achat, Fournisseur,Vente, Client, Produit
from django.db.models import Sum, F
from itertools import groupby


# Create your views here.
def vente(request):
    # Calculate total sales amount and profit
    total_vente = Vente.objects.aggregate(total_vente=Sum(F('qteVente') * F('prixUniVente')))['total_vente'] or 0

    # Calculate profit by accessing the cost of the product through the related Produit model
    total_profit = Vente.objects.aggregate(
        total_profit=Sum(F('qteVente') * F('produit__HTProd'))
    )['total_profit'] or 0

    # Calculate top clients
    top_clients = Client.objects.annotate(
        total_vente=Sum(F('vente__qteVente') * F('vente__prixUniVente'))
    ).order_by('-total_vente')[:5]

    # Calculate best-selling products
    best_sellers = Produit.objects.annotate(
        total_vente=Sum(F('vente__qteVente'))
    ).order_by('-total_vente')[:5]

    return render(request, 'dash/vente.html', {
        'total_vente': total_vente,
        'total_profit': total_profit,
        'top_clients': top_clients,
        'best_sellers': best_sellers,
    })


def achat(request):
    fournisseurs = Fournisseur.objects.all()
    
    # Calculate total amount for each fournisseur
    montantDesFournisseurs = [
        {
            'fournisseur': fournisseur,
            'montant': Achat.objects.filter(fournisseur=fournisseur).aggregate(
                total_montant=Sum(F('qteAchat') * F('HTAchat'))
            )['total_montant'] or 0
        }
        for fournisseur in fournisseurs
    ]
    
    # Sort fournisseurs by montant in descending order
    topFournisseurs = sorted(montantDesFournisseurs, key=lambda x: x['montant'], reverse=True)[:5]  # top 5
    
    # Grouping achats by year
    grouped_achats = {
        year: list(group)
        for year, group in groupby(sorted(Achat.objects.all(), key=lambda x: x.dateAchat.year, reverse=True), key=lambda x: x.dateAchat.year)
    }
    
    montantDesAchats = [
        {
            'year': year,
            'montant': sum(
                achat.qteAchat * achat.HTAchat 
                for achat in group
            ),
        }
        for year, group in grouped_achats.items()
    ]
    
    montantDesAchats_sum = sum(item['montant'] for item in montantDesAchats)
    
    return render(request, 'dash/achat.html', {'achats': montantDesAchats, 'montant': montantDesAchats_sum, 'topFournisseurs': topFournisseurs})

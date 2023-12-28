from django.shortcuts import render
from magasin.models import Achat, ProduitAchat, Fournisseur
from django.db.models import Sum, F
from itertools import groupby


# Create your views here.

def vente(request):
    return render(request,'dash/vente.html')


def achat(request):
    fournisseurs = Fournisseur.objects.all()
    
    # Calculate montant for each fournisseur
    montantDesFournisseurs = [
        {
            'fournisseur': fournisseur,
            'montant': ProduitAchat.objects.filter(achat__fournisseur=fournisseur).aggregate(
                total_montant=Sum(F('qteAchat') * F('HTAchat'))
            )['total_montant'] or 0
        }
        for fournisseur in fournisseurs
    ]
    
    # Sort fournisseurs by montant in descending order
    topFournisseurs = sorted(montantDesFournisseurs, key=lambda x: x['montant'], reverse=True)[:10]  # top 10
    
    # Grouping achats by year
    grouped_achats = {
        year: list(group)
        for year, group in groupby(sorted(Achat.objects.all(), key=lambda x: x.dateAchat.year, reverse=True), key=lambda x: x.dateAchat.year)
    }
    
    montantDesAchats = [
        {
            'year': year,
            'montant': sum(
                produit.qteAchat * produit.HTAchat 
                for achat in group for produit in ProduitAchat.objects.filter(achat=achat)
            ),
        }
        for year, group in grouped_achats.items()
    ]
    
    montantDesAchats_sum = sum(item['montant'] for item in montantDesAchats)
    
    return render(request, 'dash/achat.html', {'achats': montantDesAchats, 'montant': montantDesAchats_sum, 'topFournisseurs': topFournisseurs})

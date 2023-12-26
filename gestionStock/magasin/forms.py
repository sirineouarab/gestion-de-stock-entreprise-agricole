from django import forms
from .models import Produit, Client, Fournisseur

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['Designation', 'qteStock', 'HTProd']
        widgets = {
        'Designation': forms.TextInput(attrs={'class':'form-control'}),
        'qteStock': forms.NumberInput(attrs={'class':'form-control'}),
        'HTProd': forms.NumberInput(attrs={'class':'form-control'})
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nomPrenomC', 'adresseC','telephoneC', 'credit']
        widgets = {
        'nomPrenomC': forms.TextInput(attrs={'class':'form-control'}),
        'adresseC': forms.TextInput(attrs={'class':'form-control'}),
        'telephoneC': forms.NumberInput(attrs={'class':'form-control'}),
        'credit': forms.NumberInput(attrs={'class':'form-control'})
        }

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nomPrenomF', 'adresseF','telephoneF', 'solde']
        widgets = {
        'nomPrenomF': forms.TextInput(attrs={'class':'form-control'}),
        'adresseF': forms.TextInput(attrs={'class':'form-control'}),
        'telephoneF': forms.NumberInput(attrs={'class':'form-control'}),
        'solde': forms.NumberInput(attrs={'class':'form-control'})
        }
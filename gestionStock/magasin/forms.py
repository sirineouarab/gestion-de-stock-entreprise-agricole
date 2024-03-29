from django import forms
from .models import Produit, Client, Fournisseur, Centre, Employe, Achat,Reglement, Transfert, PayementCredit, Vente
#from django_select2.forms import ModelSelect2Widget


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

class CentreForm(forms.ModelForm):
    class Meta:
        model = Centre
        fields = ['DesignationCentre']
        widgets = {
        'DesignationCentre': forms.TextInput(attrs={'class':'form-control'}),
        }


class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['nomPrenomE', 'adresseE','telephoneE', 'salaireJour','centre']
        widgets = {
        'nomPrenomE': forms.TextInput(attrs={'class':'form-control'}),
        'adresseE': forms.TextInput(attrs={'class':'form-control'}),
        'telephoneE': forms.NumberInput(attrs={'class':'form-control'}),
        'salaireJour': forms.NumberInput(attrs={'class':'form-control'}),
        'centre': forms.Select(attrs={'class':'form-control'}),
        }


class ReglementForm(forms.ModelForm):
    class Meta:
        model = Reglement
        fields = [ 'dateReg', 'montantReg']
        widgets = {
        'dateReg': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        'montantReg': forms.NumberInput(attrs={'class':'form-control'}),
        }
        

class AchatForm(forms.ModelForm):

    class Meta:
        model = Achat
        fields = ['PayeEntierement', 'dateAchat', 'fournisseur','produit','qteAchat','HTAchat']
        widgets = {
            'PayeEntierement': forms.CheckboxInput(attrs={'class': 'form-check-input my-2'}),
            'dateAchat': forms.DateInput(attrs={'class': 'form-control my-2', 'type': 'date'}),
            'fournisseur': forms.Select(attrs={'class': 'form-control my-2'}),
            'produit': forms.Select(attrs={'class': 'form-control my-2'}),          
            'qteAchat': forms.NumberInput(attrs={'class': 'form-control my-2'}),
            'HTAchat': forms.NumberInput(attrs={'class': 'form-control my-2'}),
        }

class TransfertForm(forms.ModelForm):
    class Meta:
        model = Transfert
        fields = ['produit', 'centre', 'dateTransfert','qteTransfert']
        widgets = {
            'produit': forms.Select(attrs={'class':'form-control my-2'}),
            'centre': forms.Select(attrs={'class':'form-control my-2'}),
            'dateTransfert': forms.DateInput(attrs={'class':'form-control my-2', 'type':'date'}),
            'qteTransfert': forms.NumberInput(attrs={'class':'form-control my-2'}),
        }


class PayementCreditForm(forms.ModelForm):
    class Meta:
        model = PayementCredit
        fields = [ 'datePayCredit', 'montantPayCredit']
        widgets = {
        'datePayCredit': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        'montantPayCredit': forms.NumberInput(attrs={'class':'form-control'}),
        }

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente

        fields = ['PayeEntierement', 'dateAchat', 'fournisseur','produit','qteAchat','HTAchat']
        widgets = {
            'PayeEntierement': forms.CheckboxInput(attrs={'class': 'form-check-input my-2'}),
            'dateAchat': forms.DateInput(attrs={'class': 'form-control my-2', 'type': 'date'}),
            'fournisseur': forms.Select(attrs={'class': 'form-control my-2'}),
            'produit': forms.Select(attrs={'class': 'form-control my-2'}),          
            'qteAchat': forms.NumberInput(attrs={'class': 'form-control my-2'}),
            'HTAchat': forms.NumberInput(attrs={'class': 'form-control my-2'}),
        }

        fields = ['PayeEnt', 'dateVente','client', 'produit', 'qteVente','prixUniVente']
        widgets = {
            'PayeEnt': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dateVente': forms.DateInput(attrs={'class': 'form-control my-2', 'type': 'date'}),
            'client': forms.Select(attrs={'class': 'form-control my-2'}),
            'produit': forms.Select(attrs={'class': 'form-control my-2'}),
            'qteVente': forms.NumberInput(attrs={'class': 'form-control my-2'}),
            'prixUniVente': forms.NumberInput(attrs={'class': 'form-control my-2'}),
        }
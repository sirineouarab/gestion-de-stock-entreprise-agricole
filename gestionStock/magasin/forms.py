from django import forms
from .models import Produit, Client, Fournisseur, Centre, Employe, Achat,Reglement

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
        'dateReg': forms.DateInput(attrs={'class':'form-control'}),
        'montantReg': forms.NumberInput(attrs={'class':'form-control'}),
        }





# class AchatForm(forms.ModelForm):
#     class Meta:
#         model = Achat, Produit
#         fields = ['PayeEntierement', 'dateAchat','fournisseur', 'produit','qteAchat','HTAchat']
#         widgets = {
#         'PayeEntierement': forms.CheckboxInput(attrs={'class':'form-control'}),
#         'dateAchat': forms.DateInput(attrs={'class':'form-control'}),
#         'fournisseur': forms.Select(attrs={'class':'form-control'}),
#         'produit': forms.Select(attrs={'class':'form-control'}),
#         'qteAchat': forms.NumberInput(attrs={'class':'form-control'}),
#         'HTAchat': forms.NumberInput(attrs={'class':'form-control'}),
#         }
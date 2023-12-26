from django import forms
from .models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['Designation', 'qteStock', 'HTProd']
        widgets = {
        'Designation': forms.TextInput(attrs={'class':'form-control'}),
        'qteStock': forms.NumberInput(attrs={'class':'form-control'}),
        'HTProd': forms.NumberInput(attrs={'class':'form-control'})
        }
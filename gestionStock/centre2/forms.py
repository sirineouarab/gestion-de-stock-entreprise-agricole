from django import forms
# centre1/forms.py
from django.forms import inlineformset_factory


from .models import Vente
class SaleForm(forms.ModelForm):
  
   class Meta:
        model = Vente
        fields = ['date', 'client', 'produit', 'qteVente','prixUniVente','prix_total']
        widgets = {
            'date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'produit': forms.Select(attrs={'class': 'form-control'}),
            'qteVente': forms.NumberInput(attrs={'class':'form-control'}),
            'prixUniVente': forms.NumberInput(attrs={'class':'form-control'}),
            
            'prix_total': forms.NumberInput(attrs={'class':'form-control'})
        }
        prix_total = forms.IntegerField(disabled=True, required=False)
# forms.py
from django import forms
# centre1/forms.py

from .models import Vente

class SaleForm(forms.ModelForm):
   date = forms.CharField()
   class Meta:
        model = Vente
        fields = ['date', 'client', 'produit', 'qteVente','prixUniVente']
   prix_total = forms.IntegerField(disabled=True, required=False)
# forms.py

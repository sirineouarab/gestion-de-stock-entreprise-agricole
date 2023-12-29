from django import forms
# centre1/forms.py

from .models import Vente

class SaleForm(forms.ModelForm):
   date = forms.CharField()
   class Meta:
        model = Vente
        fields="__all__"


# forms.py

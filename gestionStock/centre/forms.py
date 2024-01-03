from django import forms
# centre1/forms.py

from .models import Vente,Absence

class SaleForm(forms.ModelForm):
   date = forms.CharField()
   class Meta:
        model = Vente
        fields = ['date', 'client', 'produit', 'qteVente','prixUniVente']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
   prix_total = forms.IntegerField(disabled=True, required=False)
# forms.py
class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['emp', 'dateAbsence']
        widgets = {
            'dateAbsence': forms.DateInput(attrs={'type': 'date'}),
        }
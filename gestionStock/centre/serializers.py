# serializers.py
# serializers.py
from rest_framework import serializers
from .models import Vente, Produit,Client,Employe,Absence

class ProduitVenteSerializer(serializers.Serializer):
    label = serializers.CharField(source='produit__Designation')
    total_ventes = serializers.IntegerField()
    
class TopCustomerSerializer(serializers.Serializer):
    customer = serializers.CharField(source='client__nomPrenomC')
    total_purchases = serializers.IntegerField()

class AbsenceChartSerializer(serializers.Serializer):
    emp__nomPrenomE = serializers.CharField()
    total_absences = serializers.IntegerField()
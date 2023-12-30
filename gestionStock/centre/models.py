from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError

class Centre(models.Model):
    CodeCentre = models.AutoField(primary_key=True)
    DesignationCentre = models.CharField(max_length=40)

class Employe(models.Model):
    CodeE = models.AutoField(primary_key=True)
    nomPrenomE = models.CharField(max_length=60)
    adresseE = models.CharField(max_length=60)
    telephoneE = models.CharField(max_length=20)
    salaireJour = models.IntegerField()
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)

class Client(models.Model):
    CodeC = models.AutoField(primary_key=True)
    nomPrenomC = models.CharField(max_length=60)
    adresseC = models.CharField(max_length=60)
    telephoneC = models.CharField(max_length=20)
    credit = models.IntegerField()

class Produit(models.Model):
    CodeP = models.AutoField(primary_key=True)
    Designation = models.CharField(max_length=40)
    qteStock = models.PositiveIntegerField()
    HTProd = models.IntegerField()# Create your models here.
# centre1/models.py
    






def validate_date_format(value):
    try:
        # Essayez de convertir la chaîne en objet date pour valider le format
        datetime.datetime.strptime(value, '%d/%m/%y')
    except ValueError:
        raise ValidationError('Format de date invalide. Utilisez dd/mm/yy.')


class Vente(models.Model):
    CodeV = models.AutoField(primary_key=True)
    date =models.DateField()
    PayeEnt = models.BooleanField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qteVente = models.IntegerField(default=0)
    prixUniVente = models.IntegerField(default=0)
    prix_total=models.IntegerField(default=0)
 
 
class CreditPayment(models.Model):
    CodePayCredit = models.AutoField(primary_key=True)
    date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE)
from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import Sum
from magasin.models import Transfert

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
    def __str__(self):
        return self.nomPrenomE


class Absence(models.Model):
    codeA=models.AutoField(primary_key=True)
    emp=models.ForeignKey(Employe,on_delete=models.CASCADE)
    dateAbsence = models.DateField()
  
class Avance(models.Model):
    codeA=models.AutoField(primary_key=True)
    montantAvance=models.DecimalField(max_digits=15, decimal_places=2)
    dateAvance=models.DateField()
    employe=models.ForeignKey(Employe,on_delete=models.CASCADE)

    
class Client(models.Model):
    CodeC = models.AutoField(primary_key=True)
    nomPrenomC = models.CharField(max_length=60)
    adresseC = models.CharField(max_length=60)
    telephoneC = models.CharField(max_length=20)
    credit = models.IntegerField()
    def __str__(self):
        return self.nomPrenomC




class Produit(models.Model):
    produit = models.AutoField(primary_key=True)
    Designation = models.CharField(max_length=40)
    qteStock = models.PositiveIntegerField()
    HTProd = models.DecimalField(max_digits=10, decimal_places=2)# Create your models here.
    def __str__(self):
        return self.Designation







def validate_date_format(value):
    try:
        # Essayez de convertir la chaîne en objet date pour valider le format
        datetime.datetime.strptime(value, '%d/%m/%y')
    except ValueError:
        raise ValidationError('Format de date invalide. Utilisez dd/mm/yy.')


class Vente(models.Model):
    CodeV = models.AutoField(primary_key=True)
    date =models.DateField()
    PayeEnt = models.BooleanField(null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qteVente = models.IntegerField(default=0)
    prixUniVente = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    prix_total=models.IntegerField(default=0)
    def montant_total_ventes(self):
        return Vente.objects.aggregate(Sum('prix_total'))['prix_total__sum'] or 0


class CreditPayment(models.Model):
    CodePayCredit = models.AutoField(primary_key=True)
    date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE)
    



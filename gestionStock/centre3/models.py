from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import Sum
from magasin.models import Produit as ProduitTransfert

class Centre(models.Model):
    CodeCentre = models.AutoField(primary_key=True)
    DesignationCentre = models.CharField(max_length=40)
    def __str__(self):
        return self.DesignationCentre

class TransfertRecu(models.Model):
    produitTr = models.ForeignKey(ProduitTransfert, on_delete=models.CASCADE,related_name='transfertrecu_produit_tr3')
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    dateTransfert = models.DateField()
    qteTransfert = models.IntegerField()
    cost = models.IntegerField(default=0)    

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
    codeAb=models.AutoField(primary_key=True)
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
    HTProd = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.Designation

class Vente(models.Model):
    CodeV = models.AutoField(primary_key=True)
    date =models.DateField()
    PayEnt = models.BooleanField(default=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qteVente = models.IntegerField(default=0)
    prixUniVente = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    prix_total=models.IntegerField(default=0)
    montant_paye=models.IntegerField(default=0)
   
class CreditPayment(models.Model):
    CodePayCredit = models.AutoField(primary_key=True)
    date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE)
    


class Reglement(models.Model):
    CodeReg = models.AutoField(primary_key=True)
    montantReg = models.DecimalField(max_digits=10, decimal_places=2)
    dateReg = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
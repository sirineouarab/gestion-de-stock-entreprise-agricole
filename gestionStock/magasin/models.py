from django.db import models

# Create your models here.
class Centre(models.Model):
    CodeCentre = models.AutoField(primary_key=True)
    DesignationCentre = models.CharField(max_length=40)
    def __str__(self):
        return self.DesignationCentre

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
    credit = models.IntegerField(default=0)

class Fournisseur(models.Model):
    CodeF = models.AutoField(primary_key=True)
    nomPrenomF = models.CharField(max_length=60)
    adresseF = models.CharField(max_length=60)
    telephoneF = models.CharField(max_length=20)
    solde = models.IntegerField(default=0)
    def __str__(self):
        return self.nomPrenomF

class Produit(models.Model):
    CodeP = models.AutoField(primary_key=True)
    Designation = models.CharField(max_length=40)
    qteStock = models.IntegerField(default=0)
    HTProd = models.IntegerField()
    def __str__(self):
        return self.Designation

class Vente(models.Model):
    CodeV = models.AutoField(primary_key=True)
    PayeEnt = models.BooleanField()
    dateVente = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

class PayementCredit(models.Model):
    CodePayCredit = models.AutoField(primary_key=True)
    montantPayCredit = models.IntegerField()
    datePayCredit = models.DateField()
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE)

class ProduitVente(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE)
    qteVente = models.IntegerField()
    prixUniVente = models.IntegerField()

class Achat(models.Model):
    CodeAchat = models.AutoField(primary_key=True)
    PayeEntierement = models.BooleanField()
    dateAchat = models.DateField()
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)

class Reglement(models.Model):
    CodeReg = models.AutoField(primary_key=True)
    montantReg = models.IntegerField()
    dateReg = models.DateField()
    achat = models.ForeignKey(Achat, on_delete=models.CASCADE)

class ProduitAchat(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    achat = models.ForeignKey(Achat, on_delete=models.CASCADE)
    qteAchat = models.IntegerField()
    HTAchat = models.IntegerField()

class Transfert(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    dateTransfert = models.DateField()
    qteTransfert = models.IntegerField()


# Generated by Django 5.0 on 2023-12-24 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Centre',
            fields=[
                ('CodeCentre', models.AutoField(primary_key=True, serialize=False)),
                ('DesignationCentre', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('CodeC', models.AutoField(primary_key=True, serialize=False)),
                ('nomPrenomC', models.CharField(max_length=60)),
                ('adresseC', models.CharField(max_length=60)),
                ('telephoneC', models.CharField(max_length=20)),
                ('credit', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('CodeF', models.AutoField(primary_key=True, serialize=False)),
                ('nomPrenomF', models.CharField(max_length=60)),
                ('adresseF', models.CharField(max_length=60)),
                ('telephoneF', models.CharField(max_length=20)),
                ('solde', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('CodeP', models.AutoField(primary_key=True, serialize=False)),
                ('Designation', models.CharField(max_length=40)),
                ('qteStock', models.IntegerField()),
                ('HTProd', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('CodeE', models.AutoField(primary_key=True, serialize=False)),
                ('nomPrenomE', models.CharField(max_length=60)),
                ('adresseE', models.CharField(max_length=60)),
                ('telephoneE', models.CharField(max_length=20)),
                ('salaireJour', models.IntegerField()),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasin.centre')),
            ],
        ),
        migrations.CreateModel(
            name='Achat',
            fields=[
                ('CodeAchat', models.AutoField(primary_key=True, serialize=False)),
                ('PayeEntierement', models.BooleanField()),
                ('dateAchat', models.DateField()),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasin.fournisseur')),
            ],
        ),
        migrations.CreateModel(
            name='ProduitAchat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qteAchat', models.IntegerField()),
                ('HTAchat', models.IntegerField()),
                ('achat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasin.achat')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasin.produit')),
            ],
        ),
        migrations.CreateModel(
            name='Reglement',
            fields=[
                ('CodeReg', models.AutoField(primary_key=True, serialize=False)),
                ('montantReg', models.IntegerField()),
                ('dateReg', models.DateField()),
                ('achat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasin.achat')),
            ],
        ),
        migrations.CreateModel(
            name='Transfert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTransfert', models.DateField()),
                ('qteTransfert', models.IntegerField()),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasin.centre')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasin.produit')),
            ],
        ),
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('CodeV', models.AutoField(primary_key=True, serialize=False)),
                ('PayeEnt', models.BooleanField()),
                ('dateVente', models.DateField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasin.client')),
            ],
        ),
        migrations.CreateModel(
            name='ProduitVente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qteVente', models.IntegerField()),
                ('prixUniVente', models.IntegerField()),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasin.produit')),
                ('vente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasin.vente')),
            ],
        ),
        migrations.CreateModel(
            name='PayementCredit',
            fields=[
                ('CodePayCredit', models.AutoField(primary_key=True, serialize=False)),
                ('montantPayCredit', models.IntegerField()),
                ('datePayCredit', models.DateField()),
                ('vente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasin.vente')),
            ],
        ),
    ]

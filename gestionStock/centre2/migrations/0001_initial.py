# Generated by Django 5.0 on 2024-01-12 10:54

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            name='Employe',
            fields=[
                ('CodeE', models.AutoField(primary_key=True, serialize=False)),
                ('nomPrenomE', models.CharField(max_length=60)),
                ('adresseE', models.CharField(max_length=60)),
                ('telephoneE', models.CharField(max_length=20)),
                ('salaireJour', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('produit', models.AutoField(primary_key=True, serialize=False)),
                ('Designation', models.CharField(max_length=40)),
                ('qteStock', models.PositiveIntegerField()),
                ('HTProd', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Avance',
            fields=[
                ('codeA', models.AutoField(primary_key=True, serialize=False)),
                ('montantAvance', models.DecimalField(decimal_places=2, max_digits=15)),
                ('dateAvance', models.DateField()),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centre2.employe')),
            ],
        ),
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('codeA', models.AutoField(primary_key=True, serialize=False)),
                ('dateAbsence', models.DateField()),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centre2.employe')),
            ],
        ),
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('CodeV', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('PayeEnt', models.BooleanField(null=True)),
                ('qteVente', models.IntegerField(default=0)),
                ('prixUniVente', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('prix_total', models.IntegerField(default=0)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centre2.client')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centre2.produit')),
            ],
        ),
        migrations.CreateModel(
            name='CreditPayment',
            fields=[
                ('CodePayCredit', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centre2.client')),
                ('vente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centre2.vente')),
            ],
        ),
    ]
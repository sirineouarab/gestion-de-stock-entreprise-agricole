# Generated by Django 5.0 on 2024-01-23 20:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centre2', '0003_rename_codea_absence_codeab'),
        ('magasin', '0008_remove_transfert_id_transfert_codetransfert'),
    ]

    operations = [
        migrations.RenameField(
            model_name='creditpayment',
            old_name='dateP',
            new_name='date',
        ),
        migrations.AddField(
            model_name='vente',
            name='PayEnt',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='vente',
            name='montant_paye',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Reglement',
            fields=[
                ('CodeReg', models.AutoField(primary_key=True, serialize=False)),
                ('montantReg', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dateReg', models.DateField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centre2.client')),
            ],
        ),
        migrations.CreateModel(
            name='TransfertRecu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTransfert', models.DateField()),
                ('qteTransfert', models.IntegerField()),
                ('cost', models.IntegerField(default=0)),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centre2.centre')),
                ('produitTr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfertrecu_produit_tr', to='magasin.produit')),
            ],
        ),
    ]

# Generated by Django 5.0 on 2023-12-28 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasin', '0003_alter_produit_qtestock'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfert',
            name='cost',
            field=models.IntegerField(default=0),
        ),
    ]

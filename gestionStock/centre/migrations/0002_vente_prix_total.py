# Generated by Django 5.0 on 2023-12-28 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centre', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vente',
            name='prix_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]

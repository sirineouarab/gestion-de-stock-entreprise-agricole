# Generated by Django 5.0 on 2024-01-19 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centre', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vente',
            name='PayEnt',
            field=models.BooleanField(default=True),
        ),
    ]

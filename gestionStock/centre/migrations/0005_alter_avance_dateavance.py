# Generated by Django 5.0 on 2024-01-02 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centre', '0004_avance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avance',
            name='dateAvance',
            field=models.DateField(),
        ),
    ]

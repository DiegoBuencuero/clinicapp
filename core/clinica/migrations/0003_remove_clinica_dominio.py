# Generated by Django 4.2.17 on 2024-12-12 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0002_clinica_dominio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clinica',
            name='dominio',
        ),
    ]

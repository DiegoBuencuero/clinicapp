# Generated by Django 4.2.17 on 2024-12-13 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0006_paciente_clinicas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='clinicas',
            field=models.ManyToManyField(related_name='pacientes', to='clinica.clinica'),
        ),
    ]

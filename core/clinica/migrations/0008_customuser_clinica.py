# Generated by Django 4.2.17 on 2024-12-13 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0007_alter_paciente_clinicas'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='clinica',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinica.clinica'),
        ),
    ]
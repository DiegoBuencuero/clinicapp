# Generated by Django 4.2.17 on 2024-12-13 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0004_customuser_first_name_customuser_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='rubro_usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinica.rubrousuario'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
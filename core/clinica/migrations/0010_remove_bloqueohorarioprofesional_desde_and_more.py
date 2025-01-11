# Generated by Django 4.2.17 on 2025-01-11 20:24

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0009_alter_profesional_obras_sociales'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloqueohorarioprofesional',
            name='desde',
        ),
        migrations.RemoveField(
            model_name='bloqueohorarioprofesional',
            name='hasta',
        ),
        migrations.RemoveField(
            model_name='habilitacion',
            name='desde',
        ),
        migrations.RemoveField(
            model_name='habilitacion',
            name='hasta',
        ),
        migrations.AddField(
            model_name='bloqueohorarioprofesional',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2025, 1, 11, 20, 23, 24, 235945, tzinfo=datetime.timezone.utc), verbose_name='Fecha'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='habilitacion',
            name='duracion',
            field=models.IntegerField(default=15, verbose_name='Duracion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='habilitacion',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2025, 1, 11, 20, 24, 2, 329289, tzinfo=datetime.timezone.utc), verbose_name='Fecha'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='habilitacion',
            name='hora_fin',
            field=models.TimeField(default=datetime.time(20, 24, 49, 14213), verbose_name='Hora Fin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='habilitacion',
            name='hora_inicio',
            field=models.TimeField(default=datetime.time(20, 24, 55, 342016), verbose_name='Hora Inicio'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='turno',
            name='sobreturno',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='TransactionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('proceso', models.CharField(choices=[('H', 'Habilitacion profesional'), ('B', 'Bloqueo profesional')], max_length=1)),
                ('hora_inicio', models.TimeField(blank=True, null=True, verbose_name='Hora Inicio')),
                ('hora_fin', models.TimeField(blank=True, null=True, verbose_name='Hora Fin')),
                ('duracion', models.IntegerField(blank=True, null=True, verbose_name='Duracion')),
                ('profesional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinica.profesional', verbose_name='profesional')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

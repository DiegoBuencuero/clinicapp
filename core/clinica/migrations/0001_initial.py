# Generated by Django 4.2.17 on 2024-12-11 22:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='correo electrónico')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Clinica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon_social', models.CharField(max_length=100)),
                ('nombre_fantasia', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=30)),
                ('movil', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('cuit', models.CharField(max_length=50)),
                ('logo', models.ImageField(default='default.jpg', upload_to='logos')),
            ],
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ObraSocial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='nombre')),
                ('apellido', models.CharField(max_length=100, verbose_name='apellido')),
                ('fecha_nacimiento', models.DateField(verbose_name='fecha_nacimiento')),
                ('dni', models.CharField(max_length=30, verbose_name='dni')),
                ('genero', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], max_length=1)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=30)),
                ('movil', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('numero_afiliado', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=1)),
                ('obra_social', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.obrasocial', verbose_name='obra_social')),
            ],
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=2, verbose_name='codigo')),
                ('descripcion', models.CharField(max_length=100, verbose_name='descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Profesional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='nombre')),
                ('apellido', models.CharField(max_length=100, verbose_name='apellido')),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=30)),
                ('movil', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('cuit', models.CharField(max_length=50)),
                ('numero_matricula', models.CharField(max_length=30, verbose_name='numero_matricula')),
                ('estado', models.CharField(max_length=1)),
                ('clinica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.clinica', verbose_name='clinica')),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.especialidad', verbose_name='especialidad')),
                ('obras_sociales', models.ManyToManyField(to='clinica.obrasocial', verbose_name='obras_sociales')),
            ],
        ),
        migrations.CreateModel(
            name='RubroUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=2)),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50, verbose_name='descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='fecha')),
                ('hora', models.TimeField(verbose_name='hora')),
                ('estado', models.CharField(max_length=1)),
                ('notas', models.TextField(blank=True, null=True, verbose_name='notas')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.paciente', verbose_name='paciente')),
                ('profesional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.profesional', verbose_name='profesional')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='paciente',
            name='tipo_documento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinica.tipodocumento', verbose_name='tipo_documento'),
        ),
        migrations.CreateModel(
            name='HorarioProfesional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dow', models.CharField(choices=[('D', 'Domingo'), ('L', 'Lunes'), ('M', 'Martes'), ('m', 'Miercoles'), ('J', 'Jueves'), ('V', 'Viernes')], max_length=1)),
                ('hora_inicio', models.TimeField(verbose_name='Hora Inicio')),
                ('hora_fin', models.TimeField(verbose_name='Hora Fin')),
                ('duracion', models.IntegerField(verbose_name='Duracion')),
                ('profesional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.profesional', verbose_name='Profesional')),
            ],
        ),
        migrations.CreateModel(
            name='Habilitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desde', models.DateField(verbose_name='Desde')),
                ('hasta', models.DateField(verbose_name='Hasta')),
                ('profesional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.profesional', verbose_name='profesional')),
            ],
        ),
        migrations.AddField(
            model_name='clinica',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.pais'),
        ),
        migrations.CreateModel(
            name='BloqueoHorarioProfesional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desde', models.DateField(verbose_name='Desde')),
                ('hasta', models.DateField(verbose_name='Hasta')),
                ('Profesional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.profesional', verbose_name='Profesional')),
            ],
        ),
    ]

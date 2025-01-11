from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class RubroUsuario(models.Model):
    def __str__(self):
        return str(self.descripcion)
    codigo = models.CharField(max_length=2)
    descripcion = models.CharField(max_length=50)

class Pais(models.Model):
    def __str__(self):
        return self.descripcion
    codigo = models.CharField( max_length=2, verbose_name=_("codigo") )
    descripcion = models.CharField( max_length=100, verbose_name=_("descripcion"))

class Clinica(models.Model):
    def __str__(self):
        return str(self.razon_social)
    razon_social = models.CharField(max_length=100)
    nombre_fantasia = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)
    movil = models.CharField(max_length=30)
    email = models.EmailField()
    cuit = models.CharField(max_length=50)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    logo = models.ImageField(default='default.jpg', upload_to='logos')

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('El correo electrónico es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superusuario debe tener is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_('correo electrónico'))
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Requerido para admin
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, verbose_name=_('nombre'), blank=True)
    last_name = models.CharField(max_length=30, verbose_name=_('apellido'), blank=True)
    objects = CustomUserManager()
    rubro_usuario = models.ForeignKey(RubroUsuario, on_delete=models.CASCADE, blank = True, null=True)
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE, blank = True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Retorna True si el usuario tiene un permiso específico.
        """
        return True  # Cambiar según necesidades

    def has_module_perms(self, app_label):
        """
        Retorna True si el usuario tiene permisos en una app específica.
        """
        return True  # Cambiar según necesidades



class ObraSocial(models.Model):
    def __str__(self):
        return str(self.nombre)
    nombre = models.CharField(max_length=100, verbose_name=_('Nombre'))

class Especialidad(models.Model):
    def __str__(self):
        return str(self.nombre)
    nombre = models.CharField(max_length=100)

class Profesional(models.Model):
    def __str__(self):
        return self.apellido + ', ' + self.nombre
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE, verbose_name=_("clinica"))
    nombre = models.CharField(max_length=100, verbose_name=_('nombre'))
    apellido = models.CharField(max_length=100, verbose_name=_('apellido'))
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, verbose_name=_('especialidad'))
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)
    movil = models.CharField(max_length=30)
    email = models.EmailField()
    cuit = models.CharField(max_length=50)
    numero_matricula = models.CharField(max_length=30, verbose_name=_('numero_matricula'))
    estado = models.CharField(max_length=1)       
    obras_sociales = models.ManyToManyField( ObraSocial, verbose_name=_('obras_sociales'), null=True, blank=True)                                                               



class HorarioProfesional(models.Model):
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, verbose_name=_('Profesional'))
    dow = models.CharField(max_length=1, choices=[
                                                    ('D', _('Domingo')),
                                                    ('L', _('Lunes')),
                                                    ('M', _('Martes')),
                                                    ('m', _('Miercoles')),
                                                    ('J', _('Jueves')),
                                                    ('V', _('Viernes')),
                                                ]
    )
    hora_inicio = models.TimeField(verbose_name=_('Hora Inicio'))
    hora_fin = models.TimeField( verbose_name= _('Hora Fin'))
    duracion = models.IntegerField( verbose_name=_('Duracion'))

class BloqueoHorarioProfesional(models.Model):
    Profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, verbose_name=_('Profesional'))
    desde = models.DateField(verbose_name=_('Desde'))
    hasta = models.DateField(verbose_name=_('Hasta'))

class TipoDocumento(models.Model):
    def __str__(self):
        return self.descripcion
    descripcion = models.CharField(max_length=50, verbose_name=_('descripcion'))
    

class Paciente(models.Model):
    def __str__(self):
        return self.apellido + ', ' + self.nombre
    nombre = models.CharField(max_length=100, verbose_name=_('nombre'))
    apellido = models.CharField(max_length=100, verbose_name=_('apellido'))
    fecha_nacimiento = models.DateField(verbose_name=_('fecha_nacimiento'))
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, verbose_name=_('tipo_documento'), null=True, blank=True)
    dni = models.CharField(max_length=30, verbose_name=_('dni'))
    genero = models.CharField(max_length=1, choices=[
                                                        ('F', _('Femenino')),
                                                        ('M', _('Masculino')),
                                                    ]
                            )
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)
    movil = models.CharField(max_length=30)
    email = models.EmailField()
    obra_social = models.ForeignKey(ObraSocial, on_delete=models.CASCADE, verbose_name=_("obra_social"))
    numero_afiliado = models.CharField(max_length=50)
    estado = models.CharField(max_length=1)
    clinicas = models.ManyToManyField(Clinica, related_name='pacientes')


class Habilitacion(models.Model):
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, verbose_name = _("profesional"))
    desde = models.DateField(verbose_name=_('Desde'))
    hasta = models.DateField(verbose_name=_('Hasta'))

class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name=_("paciente"))
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, verbose_name = _("profesional"))
    fecha = models.DateField(verbose_name=_("fecha"))
    hora = models.TimeField(verbose_name=_("hora"))
    estado = models.CharField(max_length=1)
    notas = models.TextField(verbose_name=_("notas"), blank=True, null=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)

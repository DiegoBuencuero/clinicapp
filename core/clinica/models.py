from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class ObraSocial(models.Model):
    nombre = models.CharField(max_length=100, verbose_name=_('Nombre'))

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


class Profile(models.Model):
    def __str__(self):
        return str(self.user.username)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE, null=True, blank=True)
    rubroUsuario = models.ForeignKey(RubroUsuario, on_delete=models.CASCADE, null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)

class Profesional(models.Model):
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
    obras_sociales = models.ManyToManyField( ObraSocial, verbose_name=_('obras_sociales'))                                                               



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


class Paciente(models.Model):
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE, verbose_name=_("clinica"))
    nombre = models.CharField(max_length=100, verbose_name=_('nombre'))
    apellido = models.CharField(max_length=100, verbose_name=_('apellido'))
    fecha_nacimiento = models.DateField(verbose_name=_('fecha_nacimiento'))
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
    usuario = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

from django.contrib import admin
from .models import Clinica, Profesional, RubroUsuario, Pais, Especialidad, ObraSocial, TipoDocumento, CustomUser, Paciente
# Register your models here.
admin.site.register(Clinica)
admin.site.register(Profesional)
admin.site.register(RubroUsuario)
admin.site.register(Pais)
admin.site.register(Especialidad)
admin.site.register(ObraSocial)
admin.site.register(TipoDocumento)
admin.site.register(CustomUser)
admin.site.register(Paciente)


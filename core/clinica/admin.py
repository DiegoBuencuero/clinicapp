from django.contrib import admin
from .models import Clinica, Profesional, RubroUsuario, Pais, Especialidad, ObraSocial, TipoDocumento, CustomUser, Paciente
from .models import HorarioProfesional, Habilitacion
from django.contrib.auth.admin import UserAdmin
from .form import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.
admin.site.register(Clinica)
admin.site.register(Profesional)
admin.site.register(RubroUsuario)
admin.site.register(Pais)
admin.site.register(Especialidad)
admin.site.register(ObraSocial)
admin.site.register(TipoDocumento)
admin.site.register(Paciente)
class CustomUserAdmin(UserAdmin):
    # Formulario para crear usuarios
    add_form = CustomUserCreationForm
    # Formulario para cambiar usuarios
    form = CustomUserChangeForm
    # Modelo que se va a registrar
    model = CustomUser

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'rubro_usuario', 'clinica')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'rubro_usuario', 'clinica')}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'rubro_usuario', 'clinica', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

# Registra el modelo con el admin personalizado
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(HorarioProfesional)
admin.site.register(Habilitacion)

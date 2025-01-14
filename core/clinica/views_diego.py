from django.shortcuts import render, redirect, get_object_or_404
from .models import Clinica, Paciente, ObraSocial, RubroUsuario, Profesional, Habilitacion
from django.contrib.auth.decorators import login_required
from .form import LoginForm, SignupForm, ProfesionalABMForm, PacienteABMForm, clinicadataForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages 
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.encoding import force_bytes, force_str  
from .tokens import account_activation_token  
from django.core.mail import EmailMessage  
from django.http import HttpResponse  
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse

from .form import HabilitacionTurneraForma


@login_required
def ajax_get_prof_conf(request):
    if request.method == 'GET':
        valor = request.GET.get('profesional_id')
        respuesta = {'data': 'hola'}
        return JsonResponse(respuesta)        
        


@login_required
def ajax_get_disponibilidad_prof(request):
    if request.method == 'GET':
        prof_id = request.GET.get('profesional_id')
        mes_desde = request.GET.get('mes_desde')
        mes_hasta = request.GET.get('mes_hasta')
        habilitaciones = Habilitacion.objects.filter(profesional__id=prof_id).filter( Q(fecha__month__gte = mes_desde) & Q(fecha__month__lte = mes_hasta))
        fechas = []
        for habilitacion in habilitaciones:
            fechas.append(habilitacion.fecha)

        respuesta = {'data': fechas}
        return JsonResponse(respuesta)        

@login_required
def habilitar_turnera(request):
    usuario = request.user
    clinica = usuario.clinica
    if request.method == 'POST':
        form = HabilitacionTurneraForma(clinica, request.POST)
        if form.is_valid():
            tlf = form.save(commit=False)
            habilitadas = Habilitacion.objects.filter(profesional = tlf.cleaned_data['profesional']).filter(Q(fecha__gte = tlf.cleaned_data['fecha_desde']) & Q(fecha__lte = tlf.cleaned_data['fecha_hasta']))
            #si habilitadas.len() > 0 y esta habilitado el checkbox de borrar entonces hago el delete sino doy error
            #OJO! que si habilitadas.len() == 0 no hay que hacer ni delete ni error ni fijarse en el checkbox
            habilitadas.delete()
            #si existe algun registro en la tabla HorarioProfesional para este profesional en las fechas dadas, borrarlos
            #generar los registros den la tabla Habilitacion de acuerdo a lo que esta cargdo en HorarioProfesional dentro de las fechas del form
            #for fecha in (fecha_desde -> fecha_hasta):
            #    la fecha esta en los dias de la semana del profesional?
            #          si esta entonces grabar registro
            tlf.usuario = usuario
            tlf.proceso = 'H'
            tlf.save()


    else:
        form = HabilitacionTurneraForma(clinica)
    return render(request, 'habilitar_turnera.html', {
        'form': form,
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import  Habilitacion, HorarioProfesional, TransactionLog
from django.contrib.auth.decorators import login_required
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
from datetime import datetime, timedelta
from .form import HabilitacionTurneraForma


@login_required
def ajax_get_prof_conf(request):
    if request.method == 'GET':
        valor = request.GET.get('profesional_id')
        respuesta = {'data': 'hola'}
        #habilitaciones_previas = Habilitacion.objects.filter(profesional = profesional, fecha__gte=fecha_desde, fecha__lte = fecha_hasta)
        return JsonResponse(respuesta)        
        
@login_required
def ajax_get_disponibilidad_prof(request):
    if request.method == 'GET':
        prof_id = request.GET.get('profesional_id')
        mes_desde = request.GET.get('mes_desde')
        mes_hasta = request.GET.get('mes_hasta')
        print(prof_id)
        habilitaciones = Habilitacion.objects.filter(profesional__id=prof_id).filter( Q(fecha__month__gte = mes_desde) & Q(fecha__month__lte = mes_hasta))
        fechas = []
        print(fechas)
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
            tlog = form.save(commit=False)
            profesional = form.cleaned_data['profesional']
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            borrar_habilitaciones = form.cleaned_data['borrar_habilitaciones']

            habilitaciones_previas = Habilitacion.objects.filter(profesional = profesional, fecha__gte=fecha_desde, fecha__lte = fecha_hasta)
            if habilitaciones_previas.exists():
                if borrar_habilitaciones:
                    for borrar in habilitaciones_previas:
                        print(borrar.fecha)
                    habilitaciones_previas.delete()
                    messages.success(request, "Habilitaciones anteriores eliminadas.")
                else:
                    messages.error(request, "Existen habilitaciones previas. Active la opción de borrar para continuar.")
                    form.add_error('borrar_habilitaciones', 'Para borrar las habitaciones previas seleccione ese campo')
                    return render(request, 'habilitar_turnera.html', {'form': form})

            #horarios del profe para comparar
            horarios_profesional = HorarioProfesional.objects.filter(profesional=profesional)
            WEEKDAY_MAP = {
                0: 'L', 1: 'M', 2: 'm', 3: 'J', 4: 'V', 5: 'S', 6: 'D'
            }
            # fechas válidas
            fechas_validas = []
            for fecha in (fecha_desde + timedelta(days=i) for i in range((fecha_hasta - fecha_desde).days + 1)):
                dia_semana = WEEKDAY_MAP[fecha.weekday()]
                horario = horarios_profesional.filter(dow=dia_semana).first()
                if horario:
                    Habilitacion.objects.create(
                        profesional=profesional,
                        fecha=fecha,
                        hora_inicio=horario.hora_inicio,
                        hora_fin=horario.hora_fin,
                        duracion=horario.duracion,
                    )

            # creo um  registro  para cada fecha valida  en TransactionLog y habili
            tlog.usuario = usuario
            tlog.proceso = 'H'
            tlog.save()
            messages.success(request, "Habilitación de turnos registrada correctamente.")
        else:
            messages.error(request, "Error al procesar el formulario. Verificá los datos ingresados.")
    else:
        form = HabilitacionTurneraForma(clinica)

    return render(request, 'habilitar_turnera.html', {'form': form})
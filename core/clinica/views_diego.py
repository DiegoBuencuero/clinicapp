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
        profesional_id = request.GET.get('profesional_id')
        habilitaciones_previas = Habilitacion.objects.filter(profesional_id=profesional_id)
        lista = []
        for habili in habilitaciones_previas:
            lista.append(habili.fecha)

        respuesta = {'fechas': lista}
        
        return JsonResponse(respuesta)
        
def ajax_get_disponibilidad_prof(request):
   if request.method == 'GET':
    prof_id = request.GET.get('profesional_id')
    mes_desde = int(request.GET.get('mes_desde'))
    mes_hasta = int(request.GET.get('mes_hasta'))
    año_actual = datetime.now().year

    # Filtrar habilitaciones por meses y profesional
    habilitaciones = Habilitacion.objects.filter(
        profesional__id=prof_id,
        fecha__year=año_actual
    ).filter(
        Q(fecha__month__gte=mes_desde) & Q(fecha__month__lte=mes_hasta)
    )

    # Preparar las fechas
    fechas = [habilitacion.fecha.strftime('%Y-%m-%d') for habilitacion in habilitaciones]

    # Responder con las fechas
    return JsonResponse({'data': fechas})

@login_required
def habilitar_turnera(request):
    usuario = request.user
    clinica = usuario.clinica

    if request.method == 'POST':
        form = HabilitacionTurneraForma(clinica, request.POST)
        if form.is_valid():
            print("Formulario válido")
            print("Datos del formulario:", form.cleaned_data)
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            profesional = form.cleaned_data['profesional']
            borrar_habilitaciones = form.cleaned_data['borrar_habilitaciones']

            print("Valor de borrar_habilitaciones:", borrar_habilitaciones)

            if fecha_hasta < fecha_desde:
                messages.error(request, "La fecha hasta debe ser mayor o igual a la fecha desde.")
                form = HabilitacionTurneraForma(clinica)  
                return render(request, 'habilitar_turnera.html', {'form': form})

            habilitaciones_previas = Habilitacion.objects.filter(
                profesional=profesional,
                fecha__gte=fecha_desde,
                fecha__lte=fecha_hasta
            )

            print("Habilitaciones previas:", habilitaciones_previas.exists())

            if habilitaciones_previas.exists():
                if borrar_habilitaciones:
                    habilitaciones_previas.delete()
                    messages.error(request, "Habilitaciones anteriores eliminadas.")
                else:
                    messages.error(request, "Existen habilitaciones previas. Active la opción de borrar para continuar.")
                    form = HabilitacionTurneraForma(clinica)
                    return render(request, 'habilitar_turnera.html', {'form': form})

            # Crear nuevas habilitaciones después de borrar las anteriores
            horarios_profesional = HorarioProfesional.objects.filter(profesional=profesional)
            WEEKDAY_MAP = {
                0: 'L', 1: 'M', 2: 'm', 3: 'J', 4: 'V', 5: 'S', 6: 'D'
            }

            for fecha in (fecha_desde + timedelta(days=i) for i in range((fecha_hasta - fecha_desde).days + 1)):
                dia_semana = WEEKDAY_MAP[fecha.weekday()]
                horario = horarios_profesional.filter(dow=dia_semana).first()
                if horario:
                    nueva_habilitacion = Habilitacion.objects.create(
                        profesional=profesional,
                        fecha=fecha,
                        hora_inicio=horario.hora_inicio,
                        hora_fin=horario.hora_fin,
                        duracion=horario.duracion,
                    )
                    print(f"Habilitación creada: {nueva_habilitacion}")

            # Guardar registro del proceso en TransactionLog
            tlog = form.save(commit=False)
            tlog.usuario = usuario
            tlog.proceso = 'H'
            tlog.save()
            messages.success(request, "Habilitación de turnos registrada correctamente.")
        else:
            messages.error(request, "Error al procesar el formulario. Verificá los datos ingresados.")

        form = HabilitacionTurneraForma(clinica)

    else:
        form = HabilitacionTurneraForma(clinica)

    return render(request, 'habilitar_turnera.html', {'form': form})

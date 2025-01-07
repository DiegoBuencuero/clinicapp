from django.shortcuts import render, redirect, get_object_or_404
from .models import Clinica, Paciente, ObraSocial, RubroUsuario, Profesional
from django.contrib.auth.decorators import login_required
from .form import LoginForm, SignupForm, ProfesionalABMForm
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




# Create your views here.
def dashboard(request):
    return render (request, "dashboard.html")


def inicio(request):
    if request.user.is_authenticated and request.user.rubro_usuario.codigo == 'AC':
        return render(request, 'index.html')
    clinicas = Clinica.objects.all()
    return render (request, "landing.html", {"clinicas": clinicas})

@login_required
def clinica_detalle(request, id):
    usuario = request.user
    if usuario.rubro_usuario:
        if usuario.rubro_usuario.codigo == 'PA':
            try:
                clinica = Clinica.objects.get(id=id)
                return render(request, 'clinica_detalle.html', {'clinica': clinica})
            except Clinica.DoesNotExist:
                return render(request, 'pag_error.html')  
        else:
            if usuario.rubro_usuario.codigo == 'AC':
                return render(request, 'index.html')
            else:
                return render(request, 'pag_error.html')          
    else:
        return render(request, 'pag_error.html')          


def login_view(request):
    if request.method == 'GET':
        next_url = request.GET.get('next', '/')
        form = LoginForm()
        return render(request,'login.html', {'form': form, 'next': next_url})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        print(request.POST)
        next_url = request.POST.get('next', '/')
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request,email=email,password=password)
            if user:
                login(request, user)
                return redirect(next_url)
            else:
                form.add_error('email', 'Usuario o password no validos.')

        return render(request,'login.html',{'form': form, 'next': next_url})


def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False
            rubro = RubroUsuario.objects.get(codigo = 'PA')
            user.rubro_usuario = rubro
            user.save()
            osde = ObraSocial.objects.get(id=1)
            paciente = Paciente(nombre = form.cleaned_data['first_name'], 
                                apellido = form.cleaned_data['last_name'], 
                                fecha_nacimiento = timezone.now().date(),
                                tipo_documento = form.cleaned_data['tipo_documento'],
                                dni = form.cleaned_data['dni'],
                                genero = 'M',
                                direccion = 'lksdjflskdjf',
                                telefono = 'kdflsdkjf',
                                movil = '23874932',
                                email = form.cleaned_data['email'],
                                obra_social = osde,
                                numero_afiliado = '329320',
                                estado = '1',
                                )
            paciente.save()
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return render(request, 'checkmail.html', {'user': user}) 
    else:  
        form = SignupForm()  
    return render(request, 'signup.html', {'form': form})  


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()
        return render(request, 'activateok.html', {'user': user})
    else:  
        return HttpResponse('Activation link is invalid!')

# ---------------------------------------PACIENTE------------------------------------

@login_required
def pacientes(request):
    usuario = request.user
    if usuario.rubro_usuario.codigo != 'AC':
        return render(request, 'pag_error.html')
    clinica = usuario.clinica
    if request.method == 'GET':
        pacientes = clinica.pacientes.all()
        return render(request, 'pacientes.html', {'pacientes': pacientes})
    

# ---------------------------------------PROFESIONAL------------------------------------
@login_required
def oprofesionales(request, id=None):
    usuario = request.user

    # Validar si el usuario tiene permiso
    if usuario.rubro_usuario.codigo != 'AC':
        return render(request, 'pag_error.html')

    clinica = usuario.clinica
    profesionales = Profesional.objects.filter(clinica=clinica).order_by('apellido')
    modificacion = False

    # Si se proporciona un ID, se está en modo edición
    if id:
        profesional = get_object_or_404(Profesional, id=id)  # Manejo de excepción si no existe
        if request.method == 'POST':
            form = ProfesionalABMForm(request.POST, instance=profesional)
            if 'borrar' in request.POST and form.is_valid():
                profesional.delete()
                messages.success(request, "El profesional fue eliminado exitosamente.")
                return redirect('profesionales')
            elif form.is_valid():
                form.save()
                messages.success(request, "El profesional fue actualizado exitosamente.")
                return redirect('profesionales')
        else:
            form = ProfesionalABMForm(instance=profesional)
            modificacion = True

    else:  # Modo creación
        if request.method == 'POST':
            form = ProfesionalABMForm(request.POST)
            if form.is_valid():
                profesional = form.save(commit=False)
                profesional.clinica = clinica
                profesional.estado = 'A'  # Define estados iniciales
                profesional.save()
                messages.success(request, "El profesional fue creado exitosamente.")
                return redirect('profesionales')
            else:
                messages.error(request, "Error al crear el profesional. Revisa los datos ingresados.")
        else:
            form = ProfesionalABMForm()

    return render(request, 'profesionales.html', {
        'form': form,
        'profesionales': profesionales,
        'modificacion': modificacion
    })




@login_required
def ajax_obtener_profesionales(request):
    if request.method == 'GET':
        valor = request.GET.get('valor')
        profesionales = Profesional.objects.filter(Q(nombre__icontains=valor) | Q(apellido__icontains=valor) | Q(numero_matricula__icontains=valor))
        data =[]
        for profesional in profesionales:
            data.append({'id': profesional.id, 'nombre': profesional.nombre, 'apellido': profesional.apellido, 'especialidad_nombre':profesional.especialidad.nombre})
        response = {'status': '0', 'data': data}
        return JsonResponse(response)


@login_required
def profesionales(request, id=None):
    usuario = request.user
    if usuario.rubro_usuario.codigo != 'AC':
        return render(request, 'pag_error.html')

    clinica = usuario.clinica
    profesionales = Profesional.objects.filter(clinica=clinica).order_by('apellido')
    modificacion = False
    form = None

    if request.method == 'GET':
        if id:
            profesional = get_object_or_404(Profesional, id=id, clinica=clinica)
            form = ProfesionalABMForm(instance=profesional)
            modificacion = True
        else:
            form = ProfesionalABMForm()
    elif request.method == 'POST':
        if 'btn_baja' in request.POST:
                profesional = get_object_or_404(Profesional, id=id, clinica=clinica)     
                messages.error(request, "El profesional fue eliminado exitosamente.")
                profesional.delete()
                return redirect('profesionales')          
        elif 'btn_alta' in request.POST:
            form = ProfesionalABMForm(request.POST)
            if form.is_valid():
                profesional = form.save(commit=False)
                profesional.clinica = clinica
                profesional.estado = 'A'
                profesional.save()

                messages.success(request, "El profesional fue creado exitosamente.")
                form = ProfesionalABMForm()
        elif 'btn_modif' in request.POST:
            profesional = get_object_or_404(Profesional, id=id, clinica=clinica)
            form = ProfesionalABMForm(request.POST, instance=profesional)
            if form.is_valid():
                form.save()
                messages.warning(request, "El profesional fue modificado exitosamente.")

    return render(request, 'profesionales.html', {
        'form': form,
        'profesionales': profesionales,
        'modificacion': modificacion,
    })

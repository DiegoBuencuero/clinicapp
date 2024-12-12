from django.shortcuts import render
from .models import Clinica, Paciente, ObraSocial
from django.contrib.auth.decorators import login_required
from .form import LoginForm, SignupForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.encoding import force_bytes, force_str  
from .tokens import account_activation_token  
from django.core.mail import EmailMessage  
from django.http import HttpResponse  
from django.contrib.auth import get_user_model

# Create your views here.
def dashboard(request):
    return render (request, "dashboard.html")


def inicio(request):
    clinicas = Clinica.objects.all()
    return render (request, "landing.html", {"clinicas": clinicas})

@login_required
def clinica_detalle(request, id):
    try:
        clinica = Clinica.objects.get(id=id)
        return render(request, 'clinica_detalle.html', {'clinica': clinica})
    except Clinica.DoesNotExist:
        return render(request, 'pag_error.html')  
    

def login_view(request):

    if request.method == 'GET':
        print (request.GET)
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
        
        # form is not valid or user is not authenticated
        return render(request,'login.html',{'form': form})



def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False
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
            return HttpResponse('Please confirm your email address to complete the registration')  
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
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')

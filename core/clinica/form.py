from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm  
from .models import TipoDocumento, CustomUser, Profesional, Paciente, Clinica
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class RegularForm(Form):
    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control p_input'
    email = forms.EmailField()
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

class SignupForm(UserCreationForm):  
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    
    tipo_documento = forms.ModelChoiceField(
        queryset=TipoDocumento.objects.all(),
        label=_('Tipo de documento'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dni = forms.CharField(
        max_length=30,
        label=_('DNI'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:  
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'tipo_documento', 'dni', 'password1', 'password2')


class ProfesionalABMForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super (ProfesionalABMForm,self ).__init__(*args,**kwargs)
    class Meta:
        model = Profesional
        fields = '__all__'
        exclude = ['clinica', 'estado']


class PacienteABMForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(PacienteABMForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Paciente
        fields = '__all__' 
        exclude = ['clinicas', 'estado']  

class clinicadataForm(BaseForm):
    class Meta:
        model = Clinica
        fields = '__all__' 




class CustomUserCreationForm(forms.ModelForm):
    """
    Formulario para crear nuevos usuarios. Incluye todos los campos requeridos,
    además de una confirmación de contraseña.
    """
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'rubro_usuario', 'clinica')

    def clean_password2(self):
        # Comprueba que las dos contraseñas coincidan
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        # Guarda la contraseña de forma encriptada
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class CustomUserChangeForm(forms.ModelForm):
    """
    Formulario para actualizar usuarios. Reemplaza el campo de contraseña por un
    campo de solo lectura.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff', 'rubro_usuario', 'clinica')

    def clean_password(self):
        # Devuelve el valor inicial sin cambios
        return self.initial["password"]    
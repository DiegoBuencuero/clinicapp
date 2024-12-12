from django import forms
from django.contrib.auth.forms import UserCreationForm  
from .models import TipoDocumento, CustomUser
from django.utils.translation import gettext_lazy as _

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
    tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects.all())
    dni = forms.CharField(max_length=30, label=_('dni'))
    class Meta:  
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'tipo_documento', 'dni')  

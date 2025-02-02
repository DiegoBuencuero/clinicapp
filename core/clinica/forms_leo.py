from django.forms import ModelForm, Form
from django import forms
from .models import HorarioProfesional, Profesional
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory, BaseInlineFormSet


class HorarioProfesionalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super (HorarioProfesionalForm,self ).__init__(*args,**kwargs)
    class Meta:
        model=HorarioProfesional
        fields='__all__'
        exclude = ['profesional']

TerrenoAlquilerFormset = inlineformset_factory(Profesional, HorarioProfesional, form=HorarioProfesionalForm, extra=1)

from django.forms import ModelForm, Form
from django import forms
from .models import HorarioProfesional, Profesional
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory, BaseInlineFormSet


class HorarioProfesionalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super (HorarioProfesionalForm,self ).__init__(*args,**kwargs)
    def clean(self):
        cleaned_data = super().clean()
        if 'id' in self.errors:
            del self.errors['id']  # Eliminar error si Django lo agrega
        return cleaned_data
    class Meta:
        model=HorarioProfesional
        fields='__all__'
        exclude = ['profesional', 'id']

HorarioProfesionalFormset = inlineformset_factory(Profesional, HorarioProfesional, form=HorarioProfesionalForm, extra=1)

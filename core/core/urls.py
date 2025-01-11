"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from clinica.views import dashboard, inicio, clinica_detalle, pacientes, profesionales, habilitar_turnera
from clinica.views import login_view, signup, activate, ajax_obtener_profesionales, ajax_obtener_pacientes, clinicadata
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("dashboard", dashboard, name='daschboard'),
    path('', inicio, name='inicio'),
    path('clinica/<int:id>/', clinica_detalle, name='clinica_detalle'),
    #----------------------------PROFESIONAL-----------------------------------------------
    path('profesionales', profesionales, name='profesionales'),
    path('profesionales/<int:id>/', profesionales, name='editar_profesional'),
    path('get_prof', ajax_obtener_profesionales, name='ajax_obtener_profesionales'),

    #----------------------------PACIENTES-----------------------------------------------
    path('pacientes', pacientes, name='pacientes'),
    path('pacientes/<int:id>/', pacientes, name='editar_paciente'),
    path('get_paci', ajax_obtener_pacientes, name='ajax_obtener_pacientes'),
    #----------------------------LOGIN-----------------------------------------------
    path('login/', login_view, name='login_view'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),    
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup),
    path('activate/<uidb64>/<token>/', activate, name='activate'),  
    path('pacientes', pacientes, name='pacientes'),

  
    #----------------------------PARA ACOMODAR-----------------------------------------------
    path('cldata', clinicadata, name='clinicadata'),
    path('turneraon', habilitar_turnera, name='habilitar_turnera'),






]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

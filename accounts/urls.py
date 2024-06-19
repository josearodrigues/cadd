from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('registrar/', views.usuario_registrar, name='usuario_registrar'),
    path('login/', views.usuario_login, name='usuario_login'),
    path('logout/', views.usuario_logout, name='usuario_logout'),
    path('perfil/', views.usuario_perfil, name='usuario_perfil'),
]

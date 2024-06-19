"""cadd_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from accounts import urls as accounts_urls
from cadd import urls as cadd_urls
from accounts import views

from . import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('cadd/', include(cadd_urls, namespace='sistema')),
    path('accounts/', include(accounts_urls, namespace='accounts')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    # Caminhos para o esqueci minha senha
#    path('password_reset/', auth_views.password_reset, name='password_reset'),
#    path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
#    path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
#        auth_views.password_reset_confirm, name='password_reset_confirm'),
#    path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
    # ou esse (encontra-se funcional mas se faz necessário alterações)
    path('', include('django.contrib.auth.urls')),
]

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
urlpatterns += static(settings.STATIC_URL, ) + \
                static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

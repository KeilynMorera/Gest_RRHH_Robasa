"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from django.conf import settings
from apps.authentication import views
from django.conf.urls.static import static

#Importar vistas
from apps.authentication import views

#La URL principal / utilizará las rutas de authentication.
urlpatterns = [
    path('admin/', admin.site.urls),

    # URLs de authentication
    path('', include('apps.authentication.urls')),

    # Registro de personas
    path('personas/', views.registrar_persona, name='personas'),
    #Modificar personas
    path('personas/editar/<int:id_persona>/', views.editar_persona, name='editar_persona'),

    # Registro de empresas
    path('empresas/', views.registrar_empresa, name='empresas'),

    path('empresas/editar/<int:idEmpresa>/', views.editar_empresa, name='editar_empresa'),

    path('empresas/eliminar/<int:idEmpresa>/', views.eliminar_empresa, name='eliminar_empresa'),
]


########## Archivos multimedia (imágenes) ##########

# Si estoy en modo desarrollo (DEBUG=True),
# entonces permite acceder desde el navegador
# a los archivos guardados en la carpeta media/”.
if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
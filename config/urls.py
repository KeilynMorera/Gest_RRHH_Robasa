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
    #  Modificar empresas
    path('empresas/editar/<int:idEmpresa>/', views.editar_empresa, name='editar_empresa'),
    # Eliminar empresas
    path('empresas/eliminar/<int:idEmpresa>/', views.eliminar_empresa, name='eliminar_empresa'),

    # =========================================================
    # Registro de gerencias
    # =========================================================
    path('gerencias/',                   views.gerencias_view,        name='gerencias'),
    path('gerencias/editar/<int:pk>/',   views.editar_gerencia_view,  name='editar_gerencia'),
    path('gerencias/eliminar/<int:pk>/', views.eliminar_gerencia_view, name='eliminar_gerencia'),

    # =========================================================
    # Registro de departamentos
    # =========================================================
    path('departamentos/', views.departamentos_view, name='departamentos'),
    path('departamentos/editar/<int:pk>/', views.editar_departamento_view, name='editar_departamento'),
    path('departamentos/eliminar/<int:pk>/', views.eliminar_departamento_view, name='eliminar_departamento'),

    # =========================================================
    # Registro de puestos
    # =========================================================
    path('puestos/', views.puestos_view, name='puestos'),
    path('puestos/editar/<int:pk>/', views.editar_puesto_view, name='editar_puesto'),
    path('puestos/eliminar/<int:pk>/', views.eliminar_puesto_view, name='eliminar_puesto'),


    # =========================================================
    # Registro de compensaciones
    # =========================================================
    path('compensacion-puesto/', views.compensacion_puesto_view, name='compensacion_puesto'),
    path('compensacion-puesto/editar/<int:pk>/', views.editar_compensacion_puesto_view, name='editar_compensacion_puesto'),
    path('compensacion-puesto/eliminar/<int:pk>/', views.eliminar_compensacion_puesto_view, name='eliminar_compensacion_puesto'),

    
]


########## Archivos multimedia (imágenes) ##########

# Si estoy en modo desarrollo (DEBUG=True),
# entonces permite acceder desde el navegador
# a los archivos guardados en la carpeta media/”.
if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
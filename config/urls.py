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
    # Eliminar personas
    path('personas/eliminar/<int:id_persona>/', views.eliminar_persona, name='eliminar_persona'),

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
    path('compensacion-puesto/eliminar/<int:pk>/', views.eliminar_compensacion_puesto_view, name='eliminar_compensacion_puesto'), #Se puede quitar más adelante


    # =========================================================
    # Registro de empleados
    # =========================================================
    path('empleados/', views.registrar_empleado, name='empleados'),
    path('empleados/editar/<int:id_empleado>/', views.editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<int:id_empleado>/', views.eliminar_empleado, name='eliminar_empleado'), #Se puede quitar


    # =========================================================
    # Registro de pasantes
    # =========================================================
    path('pasantes/', views.registrar_pasante, name='pasantes'),
    path('pasantes/editar/<int:id_pasante>/', views.editar_pasante, name='editar_pasante'),



    # =========================================================
    # Registro de salario de empleados
    # =========================================================
    path('salarios/', views.registrar_salario, name='salarios'),
    path('salarios/editar/<int:id_salario>/', views.editar_salario, name='editar_salario'),
    path('obtener-compensacion-empleado/<int:id_empleado>/', views.obtener_compensacion_empleado, name='obtener_compensacion_empleado'),



    # =========================================================
    # Registro de vacante
    # =========================================================
    path('vacantes/', views.registrar_vacante, name='vacantes'),
    path('vacantes/editar/<int:id_vacante_asig>/', views.editar_vacante, name='editar_vacante'),
    path('obtener-compensacion-puesto/<int:id_puesto>/', views.obtener_compensacion_puesto, name='obtener_compensacion_puesto'),


    # =========================================================
    # Registro de vacante
    # =========================================================
    path('candidatos/', views.registrar_candidato, name='candidatos'),
    path('candidatos/editar/<int:id>/', views.editar_candidato, name='editar_candidato'),


    # =========================================================
    # Registro de solicitud de vacaciones
    # =========================================================
    path('solicitudes-vacaciones/', views.registrar_solicitud_vacacion, name='solicitudes_vacaciones'),
    path('editar-solicitud-vacacion/<int:id>/', views.editar_solicitud_vacacion, name='editar_solicitud_vacacion'),
]


########## Archivos multimedia (imágenes) ##########

# Si estoy en modo desarrollo (DEBUG=True),
# entonces permite acceder desde el navegador
# a los archivos guardados en la carpeta media/”.
if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
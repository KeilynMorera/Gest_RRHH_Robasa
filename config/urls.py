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


    # Ruta para el dashboard (pantalla de eleccion (Personas o Empleado))
    path('per_emp.html/', views.per_emp_view, name='per_emp'),

    # Registro de personas
    path('personas/', views.registrar_persona, name='personas'),
    #Modificar personas
    # Editar persona
    path("personas/editar/<int:id_persona>/", views.editar_persona, name="editar_persona"),
    # Eliminar personas
    path('personas/eliminar/<int:id_persona>/', views.eliminar_persona, name='eliminar_persona'),


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

    # =========================================================
    # CONSULTA DE SALDO DE VACACIONES
    # =========================================================
    path('guardar_saldo_vacaciones/', views.guardar_saldo_vacaciones, name='guardar_saldo_vacaciones'),
    path('editar_saldo_vacaciones/<int:id>/', views.editar_saldo_vacaciones, name='editar_saldo_vacaciones'),
    path('obtener_saldo_vacaciones/', views.obtener_saldo_vacaciones, name='obtener_saldo_vacaciones'),
    

    # =========================================================
    # CONSULTA DE ASISTENCIA
    # =========================================================
    # Guardar asistencia
    path('guardar_asistencia/', views.guardar_asistencia, name='guardar_asistencia'),
    # Editar asistencia
    path('editar_asistencia/<int:id>/', views.editar_asistencia, name='editar_asistencia'),

    # =========================================================
    # CONSULTA DE PERMISOS
    # =========================================================
    path('guardar_permiso/', views.guardar_permiso, name='guardar_permiso'),



    # =========================================================
    # VISTAS PARA ACCIONES DE PERSONAL
    # =========================================================
    
    # Ruta limpia para el paso 1 (GET y POST de cabecera)
    path('accion/gestionar/', views.registrar_cabecera_accion, name='crear_accion'),
    # RUTA CORREGIDA: Es la que recibe el ID de la cabecera una vez guardado
    path('accion/gestionar/<int:pk>/', views.registrar_cabecera_accion, name='gestionar_accion'),
    
    path("accion/guardar-detalle/<int:id_accion>/", views.guardar_accion_tipo, name="guardar_accion_tipo"),

    path("accion/obtener-salario/", views.obtener_salario_empleado, name="obtener_salario_empleado"),

    path("accion/obtener-premio/", views.obtener_premio_empleado, name="obtener_premio_empleado"),


    path("rotacion-personal/", views.rotacion_personal, name="rotacion_personal"),



    # =========================================================
    # VISTAS PARA EVALUACIONES DE PERSONAL
    # =========================================================
    # Pantalla lista / historial
    # Crear nueva evaluación (CABECERA + DETALLE)
    path('evaluaciones/nueva/', views.crear_evaluacion, name='crear_evaluacion'),
    #Crear nueva evaluación Jefatura (CABECERA + DETALLE)
    path('eva-jefatura/', views.crear_evaluacion_jefatura, name='crear_evaluacion_jefatura'),
    
    path('matriz-9box/', views.crear_matriz_9box, name='crear_matriz_9box'),

    path('dashboard-resultados/', views.dashboard_resultados, name='dashboard_resultados'),

    


    
    # Ruta para la carga inicial y el guardado de la Cabecera KPI
    path('kpi/registrar/', views.registrar_kpi_view, name='registrar_kpi'),
    
    # Ruta independiente para procesar los detalles (se conecta con el redirect de tu segunda vista)
    path('kpi/registrar-detalle/', views.registrar_kpi_detalle_view, name='registrar_kpi_detalle'),

    path('premios/nuevo/', views.crear_premio, name='crear_premio'),

    path('premios/editar/<int:id>/', views.editar_premio, name='editar_premio'),

    # ===========================
    # PREMIOS ASIGNADOS
    # ===========================
    path("kpi/premios-asignados/", views.crear_premio_asignado, name="crear_premio_asignado"),

    path('dashboard-kpi/historial/', views.historial_kpi_view, name='historial_kpi'),




    path("onboarding/", views.registrar_onboarding, name="crear_onboarding"),

    path("onboarding/<int:pk>/", views.registrar_onboarding, name="gestionar_onboarding"),

    path("onboarding/<int:pk>/detalle/", views.guardar_detalle_onboarding, name="guardar_detalle_onboarding"),




    # Ruta para el dashboard (pantalla de eleccion de offboarding)
    path('elec_Offboarding.html/', views.elec_Offboarding_view, name='elec_Offboarding'),

    # Crear proceso
    path("offboarding/", views.registrar_offboarding, name="crear_offboarding"),

    # Editar / gestionar proceso existente
    path("offboarding/<int:pk>/", views.registrar_offboarding,name="gestionar_offboarding"),

    # Dashboard del checklist
    # =========================================================
    # CHECKLIST DEL OFFBOARDING
    # =========================================================
    path("offboarding/guardar-checklist/", views.guardar_checklist_offboarding, name="guardar_checklist_offboarding"),

    path("checklist_off/ver/<int:id_check>/", views.ver_checklist_offboarding, name="ver_checklist_offboarding"),
    
    path("checklist_off/<int:id_check>/editar/", views.editar_checklist_offboarding, name="editar_checklist_offboarding"),



   path("usuarios/guardar/", views.guardar_usuario_sistema, name="guardar_usuario_sistema"),
   path("usuarios/modificar/<int:id_Admin>/", views.modificar_usuario_sistema, name="modificar_usuario_sistema"),
   path("login/", views.login_usuario, name="login_usuario"),
   path('logout/', views.cerrar_sesion, name='cerrar_sesion'),

]


########## Archivos multimedia (imágenes) ##########

# Si estoy en modo desarrollo (DEBUG=True),
# entonces permite acceder desde el navegador
# a los archivos guardados en la carpeta media/”.
if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
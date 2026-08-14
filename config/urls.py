"""
Configuración de URLs globales para el proyecto.

Define la lista 'urlpatterns' encargada de enrutar las solicitudes HTTP 
hacia las vistas (views) correspondientes dentro de las aplicaciones.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importación de vistas de la aplicación principal
from apps.authentication import views

urlpatterns = [
    # =========================================================
    # ADMINISTRACIÓN Y AUTENTICACIÓN / USUARIOS
    # =========================================================
    path('admin/', admin.site.urls),
    path('', include('apps.authentication.urls')), # Incluye las rutas del módulo auth
    
    # Control de Sesión y Navegación Base
    path("login/", views.login_usuario, name="login_usuario"),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path("inicio/", views.inicio_view, name="inicio"),

    # Gestión de Usuarios del Sistema
    path("usuarios/guardar/", views.guardar_usuario_sistema, name="guardar_usuario_sistema"),
    path("usuarios/modificar/<int:id_Admin>/", views.modificar_usuario_sistema, name="modificar_usuario_sistema"),


    # =========================================================
    # ESTRUCTURA ORGANIZACIONAL
    # =========================================================
    # Empresas
    path('empresas/', views.registrar_empresa, name='empresas'),
    path('empresas/editar/<int:idEmpresa>/', views.editar_empresa, name='editar_empresa'),
    path('empresas/eliminar/<int:idEmpresa>/', views.eliminar_empresa, name='eliminar_empresa'),

    # Gerencias
    path('gerencias/', views.gerencias_view, name='gerencias'),
    path('gerencias/editar/<int:pk>/', views.editar_gerencia_view, name='editar_gerencia'),
    path('gerencias/eliminar/<int:pk>/', views.eliminar_gerencia_view, name='eliminar_gerencia'),

    # Departamentos
    path('departamentos/', views.departamentos_view, name='departamentos'),
    path('departamentos/editar/<int:pk>/', views.editar_departamento_view, name='editar_departamento'),
    path('departamentos/eliminar/<int:pk>/', views.eliminar_departamento_view, name='eliminar_departamento'),

    # Puestos y Compensaciones de Puesto
    path('puestos/', views.puestos_view, name='puestos'),
    path('puestos/editar/<int:pk>/', views.editar_puesto_view, name='editar_puesto'),
    path('puestos/eliminar/<int:pk>/', views.eliminar_puesto_view, name='eliminar_puesto'),
    
    path('compensacion-puesto/', views.compensacion_puesto_view, name='compensacion_puesto'),
    path('compensacion-puesto/editar/<int:pk>/', views.editar_compensacion_puesto_view, name='editar_compensacion_puesto'),
    path('compensacion-puesto/eliminar/<int:pk>/', views.eliminar_compensacion_puesto_view, name='eliminar_compensacion_puesto'),


    # =========================================================
    # GESTIÓN DE PERSONAL (PERSONAS, EMPLEADOS, PASANTES)
    # =========================================================
    # Selector de tipo de registro (Dashboard intermedio)
    path('per-emp/', views.per_emp_view, name='per_emp'),

    # Personas
    path('personas/', views.registrar_persona, name='personas'),
    path('personas/editar/<int:id_persona>/', views.editar_persona, name='editar_persona'),
    path('personas/eliminar/<int:id_persona>/', views.eliminar_persona, name='eliminar_persona'),

    # Empleados
    path('empleados/', views.registrar_empleado, name='empleados'),
    path('empleados/editar/<int:id_empleado>/', views.editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<int:id_empleado>/', views.eliminar_empleado, name='eliminar_empleado'),

    # Pasantes
    path('pasantes/', views.registrar_pasante, name='pasantes'),
    path('pasantes/editar/<int:id_pasante>/', views.editar_pasante, name='editar_pasante'),

    # Salarios
    path('salarios/', views.registrar_salario, name='salarios'),
    path('salarios/editar/<int:id_salario>/', views.editar_salario, name='editar_salario'),


    # =========================================================
    # RECLUTAMIENTO Y SELECCIÓN (VACANTES Y CANDIDATOS)
    # =========================================================
    # Vacantes
    path('vacantes/', views.registrar_vacante, name='vacantes'),
    path('vacantes/editar/<int:id_vacante_asig>/', views.editar_vacante, name='editar_vacante'),

    # Candidatos
    path('candidatos/', views.registrar_candidato, name='candidatos'),
    path('candidatos/editar/<int:id>/', views.editar_candidato, name='editar_candidato'),


    # =========================================================
    # CONTROL DE TIEMPO: ASISTENCIA, PERMISOS Y VACACIONES
    # =========================================================
    # Asistencia
    path('guardar_asistencia/', views.guardar_asistencia, name='guardar_asistencia'),
    path('editar_asistencia/<int:id>/', views.editar_asistencia, name='editar_asistencia'),

    # Permisos
    path('guardar_permiso/', views.guardar_permiso, name='guardar_permiso'),

    # Vacaciones
    path('solicitudes-vacaciones/', views.registrar_solicitud_vacacion, name='solicitudes_vacaciones'),
    path('editar-solicitud-vacacion/<int:id>/', views.editar_solicitud_vacacion, name='editar_solicitud_vacacion'),
    path('guardar_saldo_vacaciones/', views.guardar_saldo_vacaciones, name='guardar_saldo_vacaciones'),
    path('editar_saldo_vacaciones/<int:id>/', views.editar_saldo_vacaciones, name='editar_saldo_vacaciones'),


    # =========================================================
    # ACCIONES Y ROTACIÓN DE PERSONAL
    # =========================================================
    path('accion/gestionar/', views.registrar_cabecera_accion, name='crear_accion'),
    path('accion/gestionar/<int:pk>/', views.registrar_cabecera_accion, name='gestionar_accion'),
    path('accion/guardar-detalle/<int:id_accion>/', views.guardar_accion_tipo, name='guardar_accion_tipo'),
    path('rotacion-personal/', views.rotacion_personal, name='rotacion_personal'),


    # =========================================================
    # DESEMPEÑO, EVALUACIONES Y KPIS
    # =========================================================
    # Evaluaciones
    path('evaluaciones/nueva/', views.crear_evaluacion, name='crear_evaluacion'),
    path('eva-jefatura/', views.crear_evaluacion_jefatura, name='crear_evaluacion_jefatura'),
    path('matriz-9box/', views.crear_matriz_9box, name='crear_matriz_9box'),
    path('dashboard-resultados/', views.dashboard_resultados, name='dashboard_resultados'),

    # KPIs
    path('kpi/registrar/', views.registrar_kpi_view, name='registrar_kpi'),
    path('kpi/registrar-detalle/', views.registrar_kpi_detalle_view, name='registrar_kpi_detalle'),
    path('dashboard-kpi/historial/', views.historial_kpi_view, name='historial_kpi'),

    # Premios e Incentivos
    path('premios/nuevo/', views.crear_premio, name='crear_premio'),
    path('premios/editar/<int:id>/', views.editar_premio, name='editar_premio'),
    path('premios-asignados/', views.guardar_premio_asignado, name='guardar_premio_asignado'),


    # =========================================================
    # ONBOARDING Y OFFBOARDING
    # =========================================================
    # Onboarding
    path('onboarding/', views.registrar_onboarding, name='crear_onboarding'),
    path('onboarding/<int:pk>/', views.registrar_onboarding, name='gestionar_onboarding'),
    path('onboarding/<int:pk>/detalle/', views.guardar_detalle_onboarding, name='guardar_detalle_onboarding'),

    # Offboarding
    path('elec-offboarding/', views.elec_Offboarding_view, name='elec_Offboarding'),
    path('offboarding/', views.registrar_offboarding, name='crear_offboarding'),
    path('offboarding/<int:pk>/', views.registrar_offboarding, name='gestionar_offboarding'),
    path('offboarding/guardar-checklist/', views.guardar_checklist_offboarding, name='guardar_checklist_offboarding'),
    path('checklist_off/ver/<int:id_check>/', views.ver_checklist_offboarding, name='ver_checklist_offboarding'),
    path('offboarding/checklist/modificar/<int:id_check>/', views.modificar_checklist_offboarding, name='modificar_checklist_offboarding'),


    # =========================================================
    # ENDPOINTS ASÍNCRONOS (AJAX / APIS INTERNAS)
    # =========================================================
    path('obtener-compensacion-empleado/<int:id_empleado>/', views.obtener_compensacion_empleado, name='obtener_compensacion_empleado'),
    path('obtener-compensacion-puesto/<int:id_puesto>/', views.obtener_compensacion_puesto, name='obtener_compensacion_puesto'),
    path('obtener-saldo-vacaciones/', views.obtener_saldo_vacaciones, name='obtener_saldo_vacaciones'),
    path('accion/obtener-salario/', views.obtener_salario_empleado, name='obtener_salario_empleado'),
    path('accion/obtener-premio/', views.obtener_premio_empleado, name='obtener_premio_empleado'),
    path('premios-asignados/monto/<int:idPremio>/<int:id_KPI>/', views.obtener_monto_liquidado, name='obtener_monto_liquidado'),


    # =========================================================
    # REPORTES GENERALES
    # =========================================================
    path('reportes/', views.modulo_reportes, name='reportes'),
]


# =========================================================
# CONFIGURACIÓN DE ARCHIVOS MULTIMEDIA EN DESARROLLO
# =========================================================
# Habilita el acceso a los archivos subidos (ej. fotos de perfil) mediante URL en entorno DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
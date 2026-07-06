from django.urls import path
from .views import home
from . import views

#Esto indica que al entrar a la raíz de esta app (/), se mostrará login.html.
urlpatterns = [
    path('', home, name='home'),

    # Ruta para el dashboard (pantalla de inicio después del login)
    path('inicio.html/', views.inicio_view, name='inicio'),

    # Ruta para el dashboard (pantalla de eleccion (Personas o Empleado))
    path('per_emp.html/', views.per_emp_view, name='per_emp'),

    # Ruta para el dashboard (pantalla de registro de personas)
    path('personas/', views.registrar_persona, name='personas'), #Listo para registrar personas, se llama a la función registrar_persona en views.py

    # Ruta para el dashboard (pantalla de registro de empresas)
    path('empresas/', views.registrar_empresa, name='empresas'),

    # Ruta para el dashboard (pantalla de eleccion (Gerencia, Departamento y Puesto))
    path('comple_Empresa.html/', views.comple_Empresa_view, name='comple_Empresa'),

    # Ruta para el dashboard (pantalla de registro de gerencia)
    path('gerencias/', views.gerencias_view, name='gerencias'),

    # Ruta para el dashboard (pantalla de registro de departamento)
    path('departamentos/', views.departamentos_view, name='departamentos'),

    # Ruta para el dashboard (pantalla de registro de puesto)
    path('puestos/', views.puestos_view, name='puestos'),

    # Ruta para el dashboard (pantalla de registro de puesto)
    path('compensacion-puesto/', views.compensacion_puesto_view, name='compensacion_puesto'),

    # Ruta para el dashboard (pantalla de registro de empleado)
    path('empleados/', views.registrar_empleado, name='empleados'),

    # Ruta para el dashboard (pantalla de registro de pasantes)
    path('pasantes/', views.registrar_pasante, name='pasantes'),

    # Ruta para el dashboard (pantalla de eleccion (Registro o Consulta de salario))
    path('salarios/', views.registrar_salario, name='salarios'),

    # Vacante candidato (para ingresar el empleado o persona interesado))
    path('reclutamiento.html/', views.reclutamiento_view, name='reclutamiento'),

    #Ruta para el dashboard (pantalla de registro de vacantes)
    path('vacantes/', views.registrar_vacante, name='vacantes'),
    
    # Ruta para el dashboard (pantalla de resgistro vacante abierta)
    path('candidatos/', views.registrar_candidato, name='candidatos'),
   
    # Ruta para el dashboard (pantalla de eleccion (Solicitud o Consulta de Vacaciones))
    path('vacaciones.html/', views.vacaciones_view, name='vacaciones'),
   
    # Ruta para el dashboard (pantalla de solicitud de vacaciones)
    path('solicitudes-vacaciones/', views.registrar_solicitud_vacacion, name='solicitudes_vacaciones'),
   
    # Ruta para el dashboard (pantalla de consulta del saldo de vacaciones)
    path('guardar_saldo_vacaciones/', views.guardar_saldo_vacaciones, name='guardar_saldo_vacaciones'),

    # Ruta para el dashboard (pantalla de eleccion (Asistencia o Permiso))
    path('elec_Asistencia.html/', views.elec_Asistencia_view, name='elec_Asistencia'),

    # Ruta para el dashboard (pantalla de registro de asistencia)
    path('guardar_asistencia/', views.guardar_asistencia, name='guardar_asistencia'),

    # Ruta para el dashboard (pantalla de registro de permiso)
    path('guardar_permiso/', views.guardar_permiso, name='guardar_permiso'),

    # Ruta para el dashboard (pantalla de acción o rotación de personal)
    path('accion_rotacion.html/', views.accion_rotacion_view, name='accion_rotacion'),

    # Ruta para el dashboard (pantalla de registro de acciones del personal)
    path('accion/gestionar/', views.registrar_cabecera_accion, name='crear_accion'),


    # Ruta para el dashboard (pantalla de registro de rotación)
    path('rotacion_Personal.html/', views.rotacion_Personal_view, name='rotacion_Personal'),


    # Ruta para el dashboard (pantalla de eleccion (Evaluación de Empleado o Jefatura))
    path('evaluaciones.html/', views.evaluaciones_view, name='evaluaciones'),

    # Ruta para el dashboard (pantalla de registro de evaluación de empleados)
    path('evaluaciones/nueva/', views.crear_evaluacion, name='crear_evaluacion'),

    # Ruta para el dashboard (pantalla de registro de evaluación de jefatura)
    path('eva-jefatura/', views.crear_evaluacion_jefatura, name='crear_evaluacion_jefatura'),

    # Ruta para el dashboard (pantalla de resgistro evaluación matriz)
    path('matriz-9box/', views.crear_matriz_9box, name='crear_matriz_9box'),
    
    # Ruta para el dashboard (pantalla de vista de resultados de la evaluación)
    path('dashboard-resultados/', views.dashboard_resultados, name='dashboard_resultados'),
    
    #Ruta para el dashboard (pantalla de eleccion del tipo de componente de KPI)
    path('elec_KPI.html/', views.elec_KPI_view, name='elec_KPI'),
    
    # Ruta para el dashboard (pantalla de registro de KPI)
    path('kpi/registrar/', views.registrar_kpi_view, name='registrar_kpi'),

    # Ruta para el dashboard (pantalla de registro de KPI)
    path('premios/nuevo/', views.crear_premio, name='crear_premio'),
    
    # Ruta para el dashboard (pantalla de asignar premios a KPIs)
    path("kpi/premios-asignados/", views.crear_premio_asignado, name="crear_premio_asignado"),
  
    # Ruta para el dashboard (pantalla de configuraciones del sistema)
    path('dashboard-kpi/historial/', views.historial_kpi_view, name='historial_kpi'),

    # Ruta para el dashboard (pantalla de onboarding)
    path("onboarding/", views.registrar_onboarding, name="crear_onboarding"),





    # Ruta para el dashboard (pantalla de resgistro usuarios con permisos)
    path('usuarios.html/', views.usuarios_view, name='usuarios'),
    # Ruta para el dashboard (pantalla de configuraciones del sistema)
    path('configuraciones.html/', views.configuraciones_view, name='configuraciones'),
    # Ruta para el dashboard (pantalla de configuraciones del sistema)
    path('reportes.html/', views.reportes_view, name='reportes'),
    
    # Ruta para el dashboard (pantalla de registro de KPI)
    
    
    
    
    
    
    # Ruta para el dashboard (pantalla de eleccion de offboarding)
    path('elec_Offboarding.html/', views.elec_Offboarding_view, name='elec_Offboarding'),
    # Ruta para el dashboard (pantalla de registro de offboarding)
    path('registrar_off.html/', views.registrar_off_view, name='registrar_off'),
    # Ruta para el dashboard (pantalla de checklist de offboarding)
    path('checklist_off.html/', views.checklist_off_view, name='checklist_off'),
   
]


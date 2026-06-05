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

    
    
    
    
    
    # Ruta para el dashboard (pantalla de registro de pasantes)
    path('pasantes.html/', views.pasantes_view, name='pasantes'),
    
   

    
    
    
    # Ruta para el dashboard (pantalla de registro de salario)
    path('salario.html/', views.salario_view, name='salario'),
    # Ruta para el dashboard (pantalla de eleccion (Solicitud o Consulta de Vacaciones))
    path('vacaciones.html/', views.vacaciones_view, name='vacaciones'),
    # Ruta para el dashboard (pantalla de solicitud de vacaciones)
    path('sol_Vacacion.html/', views.sol_Vacacion_view, name='sol_Vacacion'),
    # Ruta para el dashboard (pantalla de consulta del saldo de vacaciones)
    path('con_Vacacion.html/', views.con_Vacacion_view, name='con_Vacacion'),
    # Ruta para el dashboard (pantalla de eleccion (Asistencia o Permiso))
    path('elec_Asistencia.html/', views.elec_Asistencia_view, name='elec_Asistencia'),
    # Ruta para el dashboard (pantalla de registro de asistencia)
    path('asistencia.html/', views.asistencia_view, name='asistencia'),
    # Ruta para el dashboard (pantalla de registro de permiso)
    path('permiso.html/', views.permiso_view, name='permiso'),
    # Ruta para el dashboard (pantalla de eleccion (Evaluación de Empleado o Jefatura))
    path('evaluaciones.html/', views.evaluaciones_view, name='evaluaciones'),
    # Ruta para el dashboard (pantalla de registro de evaluación de empleados)
    path('eva_Empleado.html/', views.eva_Empleado_view, name='eva_Empleado'),
    # Ruta para el dashboard (pantalla de registro de evaluación de jefatura)
    path('eva_Jefatura.html/', views.eva_Jefatura_view, name='eva_Jefatura'),
    # Ruta para el dashboard (pantalla de vista de resultados de la evaluación)
    path('result_Evaluacion.html/', views.result_Evaluacion_view, name='result_Evaluacion'),
    # Ruta para el dashboard (pantalla de resgistro evaluación matriz)
    path('matriz.html/', views.matriz_view, name='matriz'),
    # Ruta para el dashboard (pantalla de eleccion
    # (Registro Vantante (para publicación) o
    # Vacante candidato (para ingresar el empleado o persona interesado))
    path('reclutamiento.html/', views.reclutamiento_view, name='reclutamiento'),
    # Ruta para el dashboard (pantalla de resgistro vacante abierta)
    path('vacante.html/', views.vacante_view, name='vacante'),
    # Ruta para el dashboard (pantalla de resgistro vacante abierta)
    path('reclut_Vacante.html/', views.reclut_Vacante_view, name='reclut_Vacante'),
    # Ruta para el dashboard (pantalla de resgistro usuarios con permisos)
    path('usuarios.html/', views.usuarios_view, name='usuarios'),
    # Ruta para el dashboard (pantalla de configuraciones del sistema)
    path('configuraciones.html/', views.configuraciones_view, name='configuraciones'),
    # Ruta para el dashboard (pantalla de configuraciones del sistema)
    path('reportes.html/', views.reportes_view, name='reportes'),
    #Ruta para el dashboard (pantalla de eleccion del tipo de componente de KPI)
    path('elec_KPI.html/', views.elec_KPI_view, name='elec_KPI'),
    # Ruta para el dashboard (pantalla de registro de KPI)
    path('kpi_Registro.html/', views.kpi_Registro_view, name='kpi_Registro'),
    # Ruta para el dashboard (pantalla de registro de KPI)
    path('kpi_Detalle.html/', views.kpi_Detalle_view, name='kpi_Detalle'),
    # Ruta para el dashboard (pantalla de registro de KPI)
    path('kpi_Premio.html/', views.kpi_Premio_view, name='kpi_Premio'),
    # Ruta para el dashboard (pantalla de configuraciones del sistema)
    path('kpi.html/', views.kpi_view, name='kpi'),
    # Ruta para el dashboard (pantalla de onboarding)
    path('onboarding.html/', views.onboarding_view, name='onboarding'),
    # Ruta para el dashboard (pantalla de acción o rotación de personal)
    path('accion_rotacion.html/', views.accion_rotacion_view, name='accion_rotacion'),
    # Ruta para el dashboard (pantalla de acción de personal)
    path('accion_Personal.html/', views.accion_Personal_view, name='accion_Personal'),
    # Ruta para el dashboard (pantalla de rotación de personal)
    path('rotacion_Personal.html/', views.rotacion_Personal_view, name='rotacion_Personal'),
    # Ruta para el dashboard (pantalla de eleccion de offboarding)
    path('elec_Offboarding.html/', views.elec_Offboarding_view, name='elec_Offboarding'),
    # Ruta para el dashboard (pantalla de registro de offboarding)
    path('registrar_off.html/', views.registrar_off_view, name='registrar_off'),
    # Ruta para el dashboard (pantalla de checklist de offboarding)
    path('checklist_off.html/', views.checklist_off_view, name='checklist_off'),
    # Ruta para el dashboard (pantalla de asignar premios a KPIs)
    path('kpi_AsigPremio.html/', views.kpi_AsigPremio_view, name='kpi_AsigPremio'),
]


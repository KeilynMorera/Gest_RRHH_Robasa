from django.urls import path
from . import views

# ==============================================================================
# ENRUTADOR PRINCIPAL DE LA APLICACIÓN (URLS)
# Configuración y organización modular de las rutas del sistema de Gestión Humana
# ==============================================================================

urlpatterns = [

    # --------------------------------------------------------------------------
    # 1. INICIO Y AUTENTICACIÓN
    # --------------------------------------------------------------------------
    # Ruta raíz (/): Redirige o muestra la pantalla principal / Login
    path('', views.home, name='home'),
    
    # Pantalla principal del sistema tras iniciar sesión
    path('inicio/', views.inicio_view, name='inicio'),
    
    # Inicio y cierre de sesión de usuarios
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),


    # --------------------------------------------------------------------------
    # 2. ESTRUCTURA ORGANIZACIONAL Y CONFIGURACIÓN DE EMPRESA
    # --------------------------------------------------------------------------
    # Menú de selección para Empresa (Gerencia, Departamento y Puesto)
    path('empresa/menu-estructura/', views.comple_Empresa_view, name='comple_Empresa'),
    
    # Gestión de la estructura jerárquica
    path('empresas/', views.registrar_empresa, name='empresas'),
    path('gerencias/', views.gerencias_view, name='gerencias'),
    path('departamentos/', views.departamentos_view, name='departamentos'),
    path('puestos/', views.puestos_view, name='puestos'),
    path('compensacion-puesto/', views.compensacion_puesto_view, name='compensacion_puesto'),


    # --------------------------------------------------------------------------
    # 3. GESTIÓN DE EXPEDIENTES Y PERSONAL
    # --------------------------------------------------------------------------
    # Menú de navegación rápida (Personas vs. Empleados)
    path('personal/menu-personas-empleados/', views.per_emp_view, name='per_emp'),
    
    # Registro de personas, colaboradores y pasantes
    path('personas/', views.registrar_persona, name='personas'),
    path('empleados/', views.registrar_empleado, name='empleados'),
    path('pasantes/', views.registrar_pasante, name='pasantes'),


    # --------------------------------------------------------------------------
    # 4. NOMINA Y SALARIOS
    # --------------------------------------------------------------------------
    # Menú y registro/consulta de estructuras salariales
    path('salarios/', views.registrar_salario, name='salarios'),


    # --------------------------------------------------------------------------
    # 5. RECLUTAMIENTO Y SELECCIÓN DE PERSONAL
    # --------------------------------------------------------------------------
    # Menú de reclutamiento (Postulación de candidatos / Empleados)
    path('reclutamiento/menu/', views.reclutamiento_view, name='reclutamiento'),
    
    # Gestión de plazas vacantes y candidatos
    path('vacantes/', views.registrar_vacante, name='vacantes'),
    path('candidatos/', views.registrar_candidato, name='candidatos'),


    # --------------------------------------------------------------------------
    # 6. GESTIÓN DE TIEMPO: VACACIONES, ASISTENCIA Y PERMISOS
    # --------------------------------------------------------------------------
    # Menú principal del módulo de vacaciones
    path('vacaciones/menu/', views.vacaciones_view, name='vacaciones'),
    path('vacaciones/solicitudes/', views.registrar_solicitud_vacacion, name='solicitudes_vacaciones'),
    path('vacaciones/saldo/guardar/', views.guardar_saldo_vacaciones, name='guardar_saldo_vacaciones'),

    # Menú y gestión de asistencias/licencias
    path('asistencia/menu/', views.elec_Asistencia_view, name='elec_Asistencia'),
    path('asistencia/guardar/', views.guardar_asistencia, name='guardar_asistencia'),
    path('permisos/guardar/', views.guardar_permiso, name='guardar_permiso'),


    # --------------------------------------------------------------------------
    # 7. MOVIMIENTOS, ACCIONES DE PERSONAL Y ROTACIÓN
    # --------------------------------------------------------------------------
    # Menú de selección entre Acciones de Personal y Rotación
    path('movimientos/menu-accion-rotacion/', views.accion_rotacion_view, name='accion_rotacion'),
    
    # Procesamiento de acciones del personal e historial de rotación
    path('accion/gestionar/', views.registrar_cabecera_accion, name='crear_accion'),
    path('rotacion-personal/', views.rotacion_personal, name='rotacion_personal'),


    # --------------------------------------------------------------------------
    # 8. EVALUACIÓN DEL DESEMPEÑO Y DESARROLLO (MATRIZ 9-BOX)
    # --------------------------------------------------------------------------
    # Menú principal de evaluaciones
    path('evaluaciones/menu/', views.evaluaciones_view, name='evaluaciones'),
    
    # Registro de evaluaciones operativas y de jefatura
    path('evaluaciones/nueva/', views.crear_evaluacion, name='crear_evaluacion'),
    path('evaluaciones/jefatura/', views.crear_evaluacion_jefatura, name='crear_evaluacion_jefatura'),
    
    # Análisis de potencial y desempeño (9-Box y Dashboard de Resultados)
    path('evaluaciones/matriz-9box/', views.crear_matriz_9box, name='crear_matriz_9box'),
    path('evaluaciones/dashboard-resultados/', views.dashboard_resultados, name='dashboard_resultados'),


    # --------------------------------------------------------------------------
    # 9. GESTIÓN DE KPIS, METAS Y INCENTIVOS (PREMIOS)
    # --------------------------------------------------------------------------
    # Menú de selección de componentes de KPI
    path('kpis/menu/', views.elec_KPI_view, name='elec_KPI'),
    path('kpis/registrar/', views.registrar_kpi_view, name='registrar_kpi'),
    path('kpis/historial/', views.historial_kpi_view, name='historial_kpi'),
    
    # Configuración e incentivos vinculados a los KPIs
    path('premios/nuevo/', views.crear_premio, name='crear_premio'),
    path('premios/asignados/', views.guardar_premio_asignado, name='guardar_premio_asignado'),


    # --------------------------------------------------------------------------
    # 10. ONBOARDING Y OFFBOARDING (CICLO DE VIDA DEL EMPLEADO)
    # --------------------------------------------------------------------------
    # Menú y registro de incorporación (Onboarding)
    path('onboarding/', views.registrar_onboarding, name='crear_onboarding'),
    
    # Menú, registro y control de checklist de salida (Offboarding)
    path('offboarding/menu/', views.elec_Offboarding_view, name='elec_Offboarding'),
    path('offboarding/', views.registrar_offboarding, name='crear_offboarding'),
    path('offboarding/guardar-checklist/', views.guardar_checklist_offboarding, name='guardar_checklist_offboarding'),


    # --------------------------------------------------------------------------
    # 11. SEGURIDAD, REPORTES Y CONFIGURACIÓN DEL SISTEMA
    # --------------------------------------------------------------------------
    # Administración de usuarios y accesos al sistema
    path('usuarios/guardar/', views.guardar_usuario_sistema, name='guardar_usuario_sistema'),
    
    # Configuración general y reportes consolidados
    path('configuraciones/', views.configuraciones_view, name='configuraciones'),
    path('reportes/', views.modulo_reportes, name='reportes'),
]
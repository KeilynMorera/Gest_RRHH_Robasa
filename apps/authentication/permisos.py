# apps/authentication/permisos.py

# ==============================================================================
# CONFIGURACIÓN DE ROLES Y MATRIZ DE PERMISOS (RBAC)
# Define los accesos por módulo y acción permitida (ver, crear, editar, eliminar)
# para cada rol del sistema de Gestión Humana.
# ==============================================================================

PERMISOS_POR_ROL = {

    # --------------------------------------------------------------------------
    # 1. ADMINISTRADOR GLOBAL
    # Acceso total a la configuración del sistema, gestión de usuarios y 
    # control operativo completo de todos los módulos.
    # --------------------------------------------------------------------------
    "Administrador Global": {
        "usuarios_sistema":          ("ver", "crear", "editar"),
        "empresas":                  ("ver", "crear", "editar", "eliminar"),
        "estructura_organizacional": ("ver", "crear", "editar", "eliminar"),
        "empleados":                 ("ver", "crear", "editar", "eliminar"),
        "salarios":                  ("ver", "crear", "editar"),
        "reclutamiento":             ("ver", "crear", "editar"),
        "vacaciones":                ("ver", "crear", "editar"),
        "asistencia":                ("ver", "crear", "editar"),
        "permisos":                  ("ver", "crear"),
        "acciones_personal":         ("ver", "crear"),
        "evaluaciones":              ("ver", "crear"),
        "kpi":                       ("ver", "crear"),
        "premios":                   ("ver", "crear", "editar"),
        "onboarding":                ("ver", "crear"),
        "offboarding":               ("ver", "crear", "editar"),
    },

    # --------------------------------------------------------------------------
    # 2. GESTOR DE TALENTO HUMANO
    # Enfocado en la gestión operativa de personal, nómina, reclutamiento y 
    # desempeño. Solo lectura en configuraciones estructurales básicas.
    # --------------------------------------------------------------------------
    "Gestor de Talento Humano": {
        "empresas":                  ("ver",),
        "estructura_organizacional": ("ver",),
        "empleados":                 ("ver", "crear", "editar", "eliminar"),
        "salarios":                  ("ver", "crear", "editar"),
        "reclutamiento":             ("ver", "crear", "editar"),
        "vacaciones":                ("ver", "crear", "editar"),
        "asistencia":                ("ver", "crear", "editar"),
        "permisos":                  ("ver", "crear"),
        "acciones_personal":         ("ver", "crear"),
        "evaluaciones":              ("ver", "crear"),
        "kpi":                       ("ver", "crear"),
        "premios":                   ("ver", "crear", "editar"),
        "onboarding":                ("ver", "crear"),
        "offboarding":               ("ver", "crear", "editar"),
    },

    # --------------------------------------------------------------------------
    # 3. JEFATURA / SUPERVISOR
    # Acceso operativo limitado a la gestión y evaluación de su personal a cargo.
    # Nota: El filtrado por departamento o equipo se aplica en las vistas.
    # --------------------------------------------------------------------------
    "Jefatura / Supervisor": {
        "empleados":         ("ver",),            # Filtrado por su departamento en la vista
        "vacaciones":        ("ver",),
        "asistencia":        ("ver", "crear"),
        "permisos":          ("ver", "crear"),
        "evaluaciones":      ("ver", "crear"),
        "acciones_personal": ("ver", "crear"),
        "kpi":               ("ver",),
    },

    # --------------------------------------------------------------------------
    # 4. SOPORTE TÉCNICO TI
    # Perfil técnico destinado al mantenimiento de credenciales y cuentas de usuario,
    # con visibilidad restringida sobre datos de negocio/RRHH.
    # --------------------------------------------------------------------------
    "Soporte Técnico TI": {
        "usuarios_sistema": ("ver", "crear", "editar"),
        "empresas":         ("ver",),
    },

    # --------------------------------------------------------------------------
    # 5. AUDITOR / SOLO LECTURA
    # Perfil de consulta general y auditoría. Permite inspeccionar registros de 
    # todos los módulos sin privilegios de modificación o creación.
    # --------------------------------------------------------------------------
    "Auditor / Solo Lectura": {
        "usuarios_sistema":          ("ver",),
        "empresas":                  ("ver",),
        "estructura_organizacional": ("ver",),
        "empleados":                 ("ver",),
        "salarios":                  ("ver",),
        "reclutamiento":             ("ver",),
        "vacaciones":                ("ver",),
        "asistencia":                ("ver",),
        "permisos":                  ("ver",),
        "acciones_personal":         ("ver",),
        "evaluaciones":              ("ver",),
        "kpi":                       ("ver",),
        "premios":                   ("ver",),
        "onboarding":                ("ver",),
        "offboarding":               ("ver",),
    },

}


# ==============================================================================
# FUNCIÓN AUXILIAR DE VERIFICACIÓN DE PERMISOS
# ==============================================================================
def tiene_permiso(rol_nombre, modulo_slug, accion):
    """
    Evalúa si un rol específico posee permisos para realizar una acción dada 
    sobre un módulo determinado del sistema.

    Argumentos:
        rol_nombre (str): Nombre del rol asignado al usuario (ej. 'Administrador Global').
        modulo_slug (str): Identificador clave del módulo (ej. 'empleados', 'vacaciones').
        accion (str): Operación a verificar ('ver', 'crear', 'editar', 'eliminar').

    Retorna:
        bool: True si la acción está expresamente autorizada en la matriz PERMISOS_POR_ROL, 
              False en caso contrario o si el rol/módulo no existe.
    """
    # Obtiene el diccionario de permisos asignado al rol (retorna dict vacío si no existe)
    modulo_permisos = PERMISOS_POR_ROL.get(rol_nombre, {})

    # Obtiene las acciones permitidas para el módulo especificado (retorna tupla vacía si no existe)
    acciones_permitidas = modulo_permisos.get(modulo_slug, ())

    # Valida si la acción requerida está contenida en la tupla de permisos autorizados
    return accion in acciones_permitidas
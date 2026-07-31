# apps/authentication/permisos.py

PERMISOS_POR_ROL = {

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

    "Jefatura / Supervisor": {
        "empleados":         ("ver",),            # filtrado por su departamento en la vista
        "vacaciones":        ("ver",),
        "asistencia":        ("ver", "crear"),
        "permisos":          ("ver", "crear"),
        "evaluaciones":      ("ver", "crear"),
        "acciones_personal": ("ver", "crear"),
        "kpi":               ("ver",),
    },

    "Soporte Técnico TI": {
        "usuarios_sistema": ("ver", "crear", "editar"),
        "empresas":         ("ver",),
    },

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


def tiene_permiso(rol_nombre, modulo_slug, accion):

    modulo_permisos = PERMISOS_POR_ROL.get(rol_nombre, {})

    acciones_permitidas = modulo_permisos.get(modulo_slug, ())

    return accion in acciones_permitidas
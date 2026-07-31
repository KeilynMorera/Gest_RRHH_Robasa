# apps/authentication/decorators.py

from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

from .permisos import tiene_permiso


# =========================================================
# DECORADOR: requiere_permiso
#
# Se coloca ENCIMA de una vista (en views.py) para
# bloquear el acceso si el rol del usuario logueado
# no tiene el permiso indicado.
#
# Uso en views.py:
#
#     @requiere_permiso("empresas", "editar")
#     def editar_empresa(request, idEmpresa):
#         ...
# =========================================================

def requiere_permiso(modulo_slug, accion):

    def decorador(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # =================================================
            # OBTENER EL ROL DEL USUARIO LOGUEADO
            # =================================================

            rol_nombre = request.session.get(
                "usuario_rol"
            )

            # =================================================
            # VALIDAR PERMISO
            # =================================================

            if not rol_nombre or not tiene_permiso(
                rol_nombre,
                modulo_slug,
                accion
            ):

                messages.error(
                    request,
                    "No tiene permisos para realizar esta acción."
                )

                return redirect("inicio")

            # =================================================
            # SI TIENE PERMISO, CONTINÚA A LA VISTA ORIGINAL
            # =================================================

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorador


# =========================================================
# FUNCIÓN: bloquear_si_no_puede
#
# Para usar DENTRO de una vista que mezcla "ver" + "crear"
# en la misma función (patrón muy común en tu views.py).
#
# Se llama solo cuando request.method == "POST", para
# chequear el permiso de "crear" antes de guardar.
#
# Uso en views.py:
#
#     @requiere_permiso("empresas", "ver")
#     def registrar_empresa(request):
#
#         if request.method == "POST":
#
#             bloqueo = bloquear_si_no_puede(request, "empresas", "crear")
#             if bloqueo:
#                 return bloqueo
#
#             # ... resto del código para guardar ...
# =========================================================

def bloquear_si_no_puede(request, modulo_slug, accion):

    rol_nombre = request.session.get(
        "usuario_rol"
    )

    if not rol_nombre or not tiene_permiso(
        rol_nombre,
        modulo_slug,
        accion
    ):

        messages.error(
            request,
            "No tiene permisos para realizar esta acción."
        )

        return redirect("inicio")

    return None
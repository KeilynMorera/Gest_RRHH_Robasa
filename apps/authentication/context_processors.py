
from .models import UsuarioSistema
from .permisos import PERMISOS_POR_ROL   # ← LÍNEA NUEVA


def usuario_logueado(request):

    # =========================================================
    # VALORES POR DEFECTO
    # =========================================================

    usuario_nombre = "Usuario"

    usuario_puesto = "Sin puesto asignado"

    usuario_foto = ""


    # =========================================================
    # OBTENER ID DEL USUARIO DE LA SESIÓN
    # =========================================================

    usuario_id = request.session.get(
        "usuario_id"
    )


    # =========================================================
    # BUSCAR USUARIO LOGUEADO
    # =========================================================

    if usuario_id:

        try:

            usuario = (
                UsuarioSistema.objects
                .select_related(
                    "idEmpleado_Admin",
                    "idEmpleado_Admin__idPersona",
                    "idEmpleado_Admin__idPuesto"
                )
                .get(
                    id_Admin=usuario_id
                )
            )


            # =================================================
            # OBTENER EMPLEADO
            # =================================================

            empleado = usuario.idEmpleado_Admin


            # =================================================
            # OBTENER PERSONA
            # =================================================

            persona = empleado.idPersona


            # =================================================
            # NOMBRE
            # =================================================

            usuario_nombre = (
                persona.Nombre_Completo
            )


            # =================================================
            # PUESTO
            # =================================================

            if empleado.idPuesto:

                usuario_puesto = (
                    empleado.idPuesto.Nombre
                )


            # =================================================
            # FOTO
            # =================================================

            if persona.Foto:

                usuario_foto = (
                    persona.Foto.url
                )


        except UsuarioSistema.DoesNotExist:

            pass


    # =========================================================
    # PERMISOS DEL ROL ACTUAL — BLOQUE NUEVO
    # =========================================================

    rol_nombre = request.session.get(
        "usuario_rol"
    )

    permisos_rol = PERMISOS_POR_ROL.get(
        rol_nombre,
        {}
    )

    permisos = {

        modulo: {

            "ver": "ver" in acciones,

            "crear": "crear" in acciones,

            "editar": "editar" in acciones,

            "eliminar": "eliminar" in acciones,

        }

        for modulo, acciones in permisos_rol.items()

    }


    # =========================================================
    # DEVOLVER INFORMACIÓN AL TEMPLATE
    # =========================================================

    return {

        "usuario_nombre":
            usuario_nombre,

        "usuario_puesto":
            usuario_puesto,

        "usuario_foto":
            usuario_foto,

        # AGREGADO
        "permisos":
            permisos,

    }

from .models import UsuarioSistema


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
    # DEVOLVER INFORMACIÓN AL TEMPLATE
    # =========================================================

    return {

        "usuario_nombre":
            usuario_nombre,

        "usuario_puesto":
            usuario_puesto,

        "usuario_foto":
            usuario_foto,

    }

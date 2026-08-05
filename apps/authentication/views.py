from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
from django.db.models import Max
from django.db.models import Sum
from datetime import date, datetime
from django.contrib import messages
from django.db import transaction
from django.db import IntegrityError
from django.utils import timezone
from django.shortcuts import render
# ── AQUÍ SE AGREGA LA IMPORTACIÓN PARA CORREGIR EL ERROR ─────────────────
from django.db.models import Avg, Sum 
from django.db.models import Q # Asegúrate de tener esta importación al inicio de tu archivo views.py
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.shortcuts import redirect

from .forms import PremioAsignadoForm

#Importa todo lo que se encuentra en el archivo models.py
#Donde se encuentran los modelos de las tablas de la base de datos
from .models import *

from .forms import *

from apps.authentication.decorators import requiere_permiso, bloquear_si_no_puede

# =========================================================
# Vista: Login
# =========================================================
def home(request):
    return render(request, 'login.html')

# =========================================================
# Vista: Inicio
# Dashboard principal del sistema
# =========================================================
def inicio_view(request):

    # =========================================================
    # 1. TOTAL DE EMPLEADOS ACTIVOS
    # =========================================================
    total_empleados = (
        Empleado.objects
        .filter(
            Activo=True
        )
        .count()
    )


    # =========================================================
    # 2. TOTAL DE PERSONAS
    # =========================================================
    total_personas = (
        Persona.objects.count()
    )


    # =========================================================
    # 3. TOTAL DE PASANTES ACTIVOS
    # =========================================================
    total_pasantes = (
        Pasante.objects
        .filter(
            Activo=True
        )
        .count()
    )


    # =========================================================
    # 4. TOTAL DE PROCESOS DE ONBOARDING
    # =========================================================
    total_onboarding = (
        Onboarding.objects.count()
    )

    # =========================================================
    # 5. TOTAL DE PROCESOS DE OFFBOARDING
    # =========================================================
    total_offboarding = (
        Offboarding.objects.count()
    )

    # =========================================================
    # 6. TOTAL DE CHECKLISTS DE OFFBOARDING
    # =========================================================
    total_checklists_offboarding = (
        OffboardingChecklist.objects.count()
    )

    # =========================================================
    # 7. PORCENTAJE PROMEDIO DE CHECKLISTS
    # =========================================================
    promedio_checklist = (
        OffboardingChecklist.objects
        .aggregate(
            promedio=Avg("pct_listo")
        )["promedio"]
        or 0
    )

    # =========================================================
    # 8. TOTAL DE KPIs REGISTRADOS
    # =========================================================
    total_kpis = (
        KpiCabecera.objects.count()
    )

    # =========================================================
    # 9. TOTAL DE DETALLES KPI
    # =========================================================
    total_detalles_kpi = (
        KpiDetalle.objects.count()
    )

    # =========================================================
    # 10. PROMEDIO DE CUMPLIMIENTO DE KPIs
    # =========================================================
    promedio_kpi = (
        KpiDetalle.objects
        .aggregate(
            promedio=Avg("pct_Alcanzado")
        )["promedio"]
        or 0
    )

    # =========================================================
    # 11. TOTAL DE PREMIOS CONFIGURADOS
    # =========================================================
    total_premios = (
        Premio.objects.count()
    )

    # =========================================================
    # 12. TOTAL DE PREMIOS ASIGNADOS
    # =========================================================
    total_premios_asignados = (
        PremioAsignado.objects.count()
    )

    # =========================================================
    # 13. MONTO TOTAL DE PREMIOS LIQUIDADOS
    # =========================================================
    monto_total_premios = (
        PremioAsignado.objects
        .aggregate(
            total=Sum("Monto_Liquidado")
        )["total"]
        or Decimal("0.00")
    )

    # =========================================================
    # 14. TOTAL DE USUARIOS DEL SISTEMA
    # =========================================================
    total_usuarios = (
        UsuarioSistema.objects.count()
    )


    # =========================================================
    # 15. USUARIOS ACTIVOS
    # =========================================================
    usuarios_activos = (
        UsuarioSistema.objects
        .filter(
            Activo=True
        )
        .count()
    )

    # =========================================================
    # 16. TOTAL DE ROLES
    # =========================================================
    total_roles = (
        Roles.objects.count()
    )

    # =========================================================
    # 17. TOTAL DE ACCIONES / ROTACIONES
    # =========================================================
    total_acciones = (
        AccionPersonal.objects.count()
    )

    # =========================================================
    # 18. TOTAL DE EVALUACIONES
    # =========================================================
    total_evaluaciones = (
        Evaluacion.objects.count()
    )

    # =========================================================
    # 19. ÚLTIMOS PROCESOS DE ONBOARDING
    # =========================================================
    ultimos_onboarding = (
        Onboarding.objects
        .select_related(
            "idEmpleado",
            "idEmpleado__idPersona",
            "idDepartamento"
        )
        .order_by(
            "-Fecha_Inicio"
        )[:5]
    )

    # =========================================================
    # 20. ÚLTIMOS PROCESOS DE OFFBOARDING
    # =========================================================
    ultimos_offboarding = (
        Offboarding.objects
        .select_related(
            "idEmpleado",
            "idEmpleado__idPersona",
            "idCausa"
        )
        .order_by(
            "-Fecha_Salida"
        )[:5]
    )

    # =========================================================
    # 21. ÚLTIMOS KPIs
    # =========================================================
    ultimos_kpis = (
        KpiCabecera.objects
        .select_related(
            "idEmpleado",
            "idEmpleado__idPersona"
        )
        .order_by(
            "-anio",
            "-mes"
        )[:5]
    )

    # =========================================================
    # 22. ÚLTIMOS PREMIOS ASIGNADOS
    # =========================================================
    ultimos_premios = (
        PremioAsignado.objects
        .select_related(
            "idPremio",
            "id_KPI",
            "id_KPI__idEmpleado",
            "id_KPI__idEmpleado__idPersona"
        )
        .order_by(
            "-Fecha_Registro"
        )[:5]
    )

    # =========================================================
    # 23. CONTEXTO
    # =========================================================
    context = {
        # =====================================================
        # RESUMEN GENERAL
        # =====================================================

        "total_empleados":
            total_empleados,

        "total_personas":
            total_personas,

        "total_pasantes":
            total_pasantes,


        # =====================================================
        # ONBOARDING / OFFBOARDING
        # =====================================================

        "total_onboarding":
            total_onboarding,

        "total_offboarding":
            total_offboarding,

        "total_checklists_offboarding":
            total_checklists_offboarding,

        "promedio_checklist":
            round(
                float(promedio_checklist),
                2
            ),


        # =====================================================
        # KPIs
        # =====================================================

        "total_kpis":
            total_kpis,

        "total_detalles_kpi":
            total_detalles_kpi,

        "promedio_kpi":
            round(
                float(promedio_kpi),
                2
            ),


        # =====================================================
        # PREMIOS
        # =====================================================

        "total_premios":
            total_premios,

        "total_premios_asignados":
            total_premios_asignados,

        "monto_total_premios":
            monto_total_premios,


        # =====================================================
        # USUARIOS Y ROLES
        # =====================================================

        "total_usuarios":
            total_usuarios,

        "usuarios_activos":
            usuarios_activos,

        "total_roles":
            total_roles,


        # =====================================================
        # ACCIONES Y EVALUACIONES
        # =====================================================

        "total_acciones":
            total_acciones,

        "total_evaluaciones":
            total_evaluaciones,


        # =====================================================
        # ÚLTIMOS REGISTROS
        # =====================================================

        "ultimos_onboarding":
            ultimos_onboarding,

        "ultimos_offboarding":
            ultimos_offboarding,

        "ultimos_kpis":
            ultimos_kpis,

        "ultimos_premios":
            ultimos_premios,
    }

    # =========================================================
    # MOSTRAR DASHBOARD
    # =========================================================
    return render(
        request,
        "inicio.html",
        context
    )


# =========================================================
# Vista: Empresas — registro, modificación y listado
# NOTA: esta función reemplaza tanto 'registrar_empresa'
#       como 'empresas_view'. En urls.py debe quedar
#       una sola ruta apuntando aquí con name='empresas'.
# =========================================================
# =========================================================
# Vista: Empresas — registro, modificación y listado
# =========================================================
@requiere_permiso("empresas", "ver")
def registrar_empresa(request):

    print("ROL EN SESIÓN:", repr(request.session.get("usuario_rol")))

    # ─────────────────────────────────────────────
    # POST → Crear o Modificar empresa
    # ─────────────────────────────────────────────
    if request.method == 'POST':

        # ─────────────────────────────────────────────
        # BLOQUEAR SI NO PUEDE CREAR/MODIFICAR
        # ─────────────────────────────────────────────
        accion = request.POST.get('accion')

        if accion == 'modificar':
            bloqueo = bloquear_si_no_puede(request, "empresas", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "empresas", "crear")

        if bloqueo:
            return bloqueo

        empresa_id = request.POST.get('empresa_id')

        nombre_empresa = request.POST.get('nombre_empresa')
        descripcion_empresa = request.POST.get('descripcion_empresa')

        # =====================================
        # CREAR EMPRESA
        # =====================================
        if accion == 'crear' or not accion:

            Empresa.objects.create(
                Nombre=nombre_empresa,
                Descripcion=descripcion_empresa
            )

        # =====================================
        # MODIFICAR EMPRESA
        # =====================================
        elif accion == 'modificar' and empresa_id:

            empresa = Empresa.objects.get(pk=empresa_id)

            empresa.Nombre = nombre_empresa
            empresa.Descripcion = descripcion_empresa

            empresa.save()

        return redirect('empresas')

    # ─────────────────────────────────────────────
    # GET → Mostrar formulario + tabla
    # ─────────────────────────────────────────────
    return render(request, 'empresas.html', {
        'empresas': Empresa.objects.all().order_by('Nombre')
    })


# =========================================================
# Cargar empresa para edición
# =========================================================
@requiere_permiso("empresas", "editar")
def editar_empresa(request, idEmpresa):

    empresa = get_object_or_404(
        Empresa,
        pk=idEmpresa
    )

    return render(
        request,
        'empresas.html',
        {
            'empresa_editar': empresa,
            'empresas': Empresa.objects.all().order_by('Nombre')
        }
    )


# =========================================================
# Eliminar empresa
# =========================================================
@requiere_permiso("empresas", "eliminar")
def eliminar_empresa(request, idEmpresa):

    empresa = get_object_or_404(
        Empresa,
        pk=idEmpresa
    )

    empresa.delete()

    return redirect('empresas')



# =========================================================
# Vista: Elección Complementos de la Empresa: Gerencia, Departamento y Puesto
# =========================================================

def comple_Empresa_view(request):
    return render(request, 'comple_Empresa.html')


@requiere_permiso("estructura_organizacional", "ver")
def gerencias_view(request):

    if request.method == 'POST':
        gerencia_id  = request.POST.get('gerencia_id')  # vacío = nuevo registro

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN SI ES CREAR O MODIFICAR
        # ─────────────────────────────────────────────
        if gerencia_id:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "crear")

        if bloqueo:
            return bloqueo

        nombre       = request.POST.get('nombre_gerencia')
        empresa_id   = request.POST.get('empresa')
        empresa_obj  = Empresa.objects.get(pk=empresa_id)
 
        if gerencia_id:
            # Modificar registro existente
            gerencia = Gerencia.objects.get(pk=gerencia_id)
            gerencia.Nombre    = nombre
            gerencia.idEmpresa = empresa_obj
            gerencia.save()
        else:
            # Crear nuevo registro
            Gerencia.objects.create(
                Nombre    = nombre,
                idEmpresa = empresa_obj,
            )
 
        return redirect('gerencias')
 
    # GET normal: formulario vacío + tabla
    return render(request, 'gerencia.html', {
        'empresas'       : Empresa.objects.all(),
        'gerencias'      : Gerencia.objects.select_related('idEmpresa').order_by('Nombre'),
        'gerencia_editar': None,
    })
 
 
# =========================================================
# Vista: Editar gerencia — recarga el formulario con datos
# =========================================================
@requiere_permiso("estructura_organizacional", "editar")
def editar_gerencia_view(request, pk):
    gerencia = Gerencia.objects.get(pk=pk)
 
    return render(request, 'gerencia.html', {
        'empresas'       : Empresa.objects.all(),
        'gerencias'      : Gerencia.objects.select_related('idEmpresa').order_by('Nombre'),
        'gerencia_editar': gerencia,   # ← rellena el formulario
    })
 
 
# =========================================================
# Vista: Eliminar gerencia
# =========================================================
@requiere_permiso("estructura_organizacional", "eliminar")
def eliminar_gerencia_view(request, pk):
    Gerencia.objects.filter(pk=pk).delete()
    return redirect('gerencias')



@requiere_permiso("estructura_organizacional", "ver")
def departamentos_view(request):

    if request.method == 'POST':

        departamento_id = request.POST.get('departamento_id')

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN SI ES CREAR O MODIFICAR
        # ─────────────────────────────────────────────
        if departamento_id:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "crear")

        if bloqueo:
            return bloqueo

        nombre = request.POST.get('nombre_departamento')

        gerencia_id = request.POST.get('gerencia')
        gerencia_obj = Gerencia.objects.get(pk=gerencia_id)

        if departamento_id:
            # Modificar
            departamento = Departamento.objects.get(
                pk=departamento_id
            )

            departamento.Nombre = nombre
            departamento.idGerencia = gerencia_obj

            departamento.save()

        else:
            # Crear
            Departamento.objects.create(
                Nombre=nombre,
                idGerencia=gerencia_obj
            )

        return redirect('departamentos')

    # GET
    return render(
        request,
        'departamento.html',
        {
            'gerencias': Gerencia.objects.select_related(
                'idEmpresa'
            ).order_by('Nombre'),

            'departamentos': Departamento.objects.select_related(
                'idGerencia',
                'idGerencia__idEmpresa'
            ).order_by('Nombre'),

            'departamento_editar': None,
        }
    )


# =========================================================
# Vista: Editar departamento
# =========================================================
@requiere_permiso("estructura_organizacional", "editar")
def editar_departamento_view(request, pk):

    departamento = Departamento.objects.get(
        pk=pk
    )

    return render(
        request,
        'departamento.html',
        {
            'gerencias': Gerencia.objects.select_related(
                'idEmpresa'
            ).order_by('Nombre'),

            'departamentos': Departamento.objects.select_related(
                'idGerencia',
                'idGerencia__idEmpresa'
            ).order_by('Nombre'),

            'departamento_editar': departamento,
        }
    )


# =========================================================
# Vista: Eliminar departamento
# =========================================================
@requiere_permiso("estructura_organizacional", "eliminar")
def eliminar_departamento_view(request, pk):

    Departamento.objects.filter(
        pk=pk
    ).delete()

    return redirect('departamentos')



@requiere_permiso("estructura_organizacional", "ver")
def puestos_view(request):

    if request.method == 'POST':

        puesto_id = request.POST.get('puesto_id')

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN SI ES CREAR O MODIFICAR
        # ─────────────────────────────────────────────
        if puesto_id:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "crear")

        if bloqueo:
            return bloqueo

        nombre = request.POST.get('nombre_puesto')
        descripcion = request.POST.get('descripcion')

        departamento_id = request.POST.get('departamento')
        departamento_obj = Departamento.objects.get(
            pk=departamento_id
        )

        if puesto_id:

            puesto = Puesto.objects.get(
                pk=puesto_id
            )

            puesto.Nombre = nombre
            puesto.Descripcion = descripcion
            puesto.idDepartamento = departamento_obj

            puesto.save()

        else:

            Puesto.objects.create(
                Nombre=nombre,
                Descripcion=descripcion,
                idDepartamento=departamento_obj
            )

        return redirect('puestos')

    # ==========================
    # PRUEBA
    # ==========================

    departamentos = Departamento.objects.select_related(
        'idGerencia'
    ).order_by('Nombre')

    print("DEPARTAMENTOS ENVIADOS AL TEMPLATE:")

    for d in departamentos:
        print(d.id_Departamento, d.Nombre)

    # ==========================
    # GET
    # ==========================

    return render(
        request,
        'puesto.html',
        {
            'departamentos': departamentos,

            'puestos': Puesto.objects.select_related(
                'idDepartamento',
                'idDepartamento__idGerencia'
            ).order_by('Nombre'),

            'puesto_editar': None,
        }
    )


# =========================================================
# Vista: Editar puesto
# =========================================================
@requiere_permiso("estructura_organizacional", "editar")
def editar_puesto_view(request, pk):

    puesto = Puesto.objects.get(
        pk=pk
    )

    return render(
        request,
        'puesto.html',
        {
            'departamentos': Departamento.objects.select_related(
                'idGerencia'
            ).order_by('Nombre'),

            'puestos': Puesto.objects.select_related(
                'idDepartamento',
                'idDepartamento__idGerencia'
            ).order_by('Nombre'),

            'puesto_editar': puesto,
        }
    )

# =========================================================
# Vista: Eliminar puesto
# =========================================================
@requiere_permiso("estructura_organizacional", "eliminar")
def eliminar_puesto_view(request, pk):

    Puesto.objects.filter(
        pk=pk
    ).delete()

    return redirect('puestos')


@requiere_permiso("estructura_organizacional", "ver")
def compensacion_puesto_view(request):

    if request.method == 'POST':

        compensacion_id = request.POST.get('compensacion_id')

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN SI ES CREAR O MODIFICAR
        # ─────────────────────────────────────────────
        if compensacion_id:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "crear")

        if bloqueo:
            return bloqueo

        salario_bruto = request.POST.get('salario_bruto')
        salario_sem_neto = request.POST.get('salario_sem_neto')
        comision_base = request.POST.get('comision_base')
        variable_base = request.POST.get('variable_base')
        viaticos_alimenticios = request.POST.get('viaticos_alimenticios')
        kilometraje_base = request.POST.get('kilometraje_base')
        bono_base = request.POST.get('bono_base')
        vigencia = request.POST.get('vigencia')

        puesto_id = request.POST.get('puesto')
        puesto_obj = Puesto.objects.get(
            pk=puesto_id
        )

        if compensacion_id:

            # Modificar
            compensacion = Compensacion_Puesto.objects.get(
                pk=compensacion_id
            )

            compensacion.Salario_Bruto = salario_bruto
            compensacion.Salario_Sem_Neto = salario_sem_neto
            compensacion.Comision_Base = comision_base
            compensacion.Variable_Base = variable_base
            compensacion.Viaticos_Alimenticios = viaticos_alimenticios
            compensacion.Kilometraje_Base = kilometraje_base
            compensacion.Bono_Base = bono_base
            compensacion.Vigencia = vigencia
            compensacion.idPuesto = puesto_obj

            compensacion.save()

        else:

            # Crear
            Compensacion_Puesto.objects.create(
                Salario_Bruto=salario_bruto,
                Salario_Sem_Neto=salario_sem_neto,
                Comision_Base=comision_base,
                Variable_Base=variable_base,
                Viaticos_Alimenticios=viaticos_alimenticios,
                Kilometraje_Base=kilometraje_base,
                Bono_Base=bono_base,
                Vigencia=vigencia,
                idPuesto=puesto_obj
            )

        return redirect('compensacion_puesto')

    # GET
    return render(
        request,
        'confi_Puesto.html',
        {
            'puestos': Puesto.objects.select_related(
                'idDepartamento'
            ).order_by('Nombre'),

            'compensaciones': Compensacion_Puesto.objects.select_related(
                'idPuesto',
                'idPuesto__idDepartamento'
            ).order_by('-Vigencia'),

            'compensacion_editar': None,
        }
    )

# =========================================================
# Vista: Editar compensación
# =========================================================
@requiere_permiso("estructura_organizacional", "editar")
def editar_compensacion_puesto_view(request, pk):

    compensacion = Compensacion_Puesto.objects.get(
        pk=pk
    )

    return render(
        request,
         'confi_Puesto.html',
        {
            'puestos': Puesto.objects.select_related(
                'idDepartamento'
            ).order_by('Nombre'),

            'compensaciones': Compensacion_Puesto.objects.select_related(
                'idPuesto',
                'idPuesto__idDepartamento'
            ).order_by('-Vigencia'),

            'compensacion_editar': compensacion,
        }
    )

# =========================================================
# Vista: Eliminar compensación
# =========================================================
@requiere_permiso("estructura_organizacional", "eliminar")
def eliminar_compensacion_puesto_view(request, pk):
    Compensacion_Puesto.objects.filter(pk=pk).delete()
    return redirect('compensacion_puesto')   # ← mismo name que usás arriba



# =========================================================
# Vista: Elección Personas, Empleados o Pasantes
# =========================================================
def per_emp_view(request):
    return render(request, 'per_emp.html')


@requiere_permiso("empleados", "ver")
def registrar_persona(request):

    # ── POST: crear o modificar ────────────────────────────
    if request.method == 'POST':
        accion     = request.POST.get('accion')      # 'crear' o 'modificar'
        persona_id = request.POST.get('persona_id')  # vacío si es nuevo

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN LA ACCIÓN
        # ─────────────────────────────────────────────
        if accion == 'modificar':
            bloqueo = bloquear_si_no_puede(request, "empleados", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "empleados", "crear")

        if bloqueo:
            return bloqueo

        nombre     = request.POST.get('nombre_completo')
        cedula     = request.POST.get('cedula')
        sexo_id    = request.POST.get('sexo')
        nacimiento = request.POST.get('fecha_nacimiento')
        telefono   = request.POST.get('telefono')
        celular    = request.POST.get('celular')
        correo     = request.POST.get('correo')
        direccion  = request.POST.get('direccion')
        foto       = request.FILES.get('foto')

        sexo_obj = PersonaSexo.objects.get(pk=sexo_id)

        if accion == 'crear' or not accion:
            # 'not accion' mantiene compatibilidad si el botón
            # anterior no enviaba el campo 'accion'
            nueva = Persona(
                Nombre_Completo  = nombre,
                Cedula           = cedula,
                idSexo           = sexo_obj,
                Fecha_Nacimiento = nacimiento,
                Telefono         = telefono,
                Celular          = celular,
                Correo           = correo,
                Direccion        = direccion,
            )
            if foto:
                nueva.Foto = foto
            nueva.save()

        elif accion == 'modificar' and persona_id:
            persona = Persona.objects.get(pk=persona_id)
            persona.Nombre_Completo  = nombre
            persona.Cedula           = cedula
            persona.idSexo           = sexo_obj
            persona.Fecha_Nacimiento = nacimiento
            persona.Telefono         = telefono
            persona.Celular          = celular
            persona.Correo           = correo
            persona.Direccion        = direccion
            if foto:                  # solo reemplaza si se subió una nueva
                persona.Foto = foto
            persona.save()

        # Patrón PRG: redirige para evitar reenvío del form al recargar
        return redirect('personas')

    # ── GET: mostrar formulario + tabla con todos los registros ──
    return render(request, 'personas.html', {
        'sexos'   : PersonaSexo.objects.all(),
        'personas': Persona.objects.select_related('idSexo')
                                   .all()
                                   .order_by('Nombre_Completo'),
    })


@requiere_permiso("empleados", "editar")
def editar_persona(request, id_persona):

    # =========================================
    # OBTENER LA PERSONA A MODIFICAR
    # =========================================
    persona = get_object_or_404(
        Persona,
        pk=id_persona
    )

    # =========================================
    # SI PRESIONA GUARDAR CAMBIOS
    # =========================================
    if request.method == "POST":

        try:

            persona.Nombre_Completo = request.POST.get(
                "nombre_completo"
            )

            persona.Cedula = request.POST.get(
                "cedula"
            )

            persona.idSexo = PersonaSexo.objects.get(
                pk=request.POST.get("sexo")
            )

            persona.Fecha_Nacimiento = request.POST.get(
                "fecha_nacimiento"
            )

            persona.Telefono = request.POST.get(
                "telefono"
            )

            persona.Celular = request.POST.get(
                "celular"
            )

            persona.Correo = request.POST.get(
                "correo"
            )

            persona.Direccion = request.POST.get(
                "direccion"
            )

            # Solo reemplaza la foto si se seleccionó otra
            if request.FILES.get("foto"):

                persona.Foto = request.FILES["foto"]

            # Guarda los cambios
            persona.save()

            messages.success(
                request,
                "La información fue actualizada correctamente."
            )

            return redirect("personas")

        except Exception as e:

            messages.error(
                request,
                f"Ocurrió un error: {e}"
            )

    # =========================================
    # CARGAR EL FORMULARIO CON LOS DATOS
    # =========================================
    context = {

        "persona_editar": persona,

        "personas": Persona.objects.select_related(
            "idSexo"
        ).order_by(
            "Nombre_Completo"
        ),

        "sexos": PersonaSexo.objects.all()

    }

    return render(
        request,
        "personas.html",
        context
    )

# =========================================================
# Vista: Eliminar Persona
# =========================================================
@requiere_permiso("empleados", "eliminar")
def eliminar_persona(request, id_persona):
    persona = get_object_or_404(Persona, pk=id_persona)
    persona.delete()
    return redirect('personas')



# =========================================================
# Vista: Empleados — registro, modificación y listado
# =========================================================
@requiere_permiso("empleados", "ver")
def registrar_empleado(request):

    # ── POST: crear o modificar ────────────────────────────
    if request.method == 'POST':

        accion      = request.POST.get('accion')        # 'crear' o 'modificar'
        empleado_id = request.POST.get('empleado_id')   # vacío si es nuevo

        # =========================================================
        # BLOQUEAR SEGÚN LA ACCIÓN
        # =========================================================

        if accion == 'modificar':

            bloqueo = bloquear_si_no_puede(
                request,
                "empleados",
                "editar"
            )

        else:

            bloqueo = bloquear_si_no_puede(
                request,
                "empleados",
                "crear"
            )

        # Si el usuario no tiene permiso, se detiene la operación
        if bloqueo:
            return bloqueo

        # =========================================================
        # OBTENER DATOS DEL FORMULARIO
        # =========================================================

        persona_id    = request.POST.get('persona')
        puesto_id     = request.POST.get('puesto')
        contrato_id   = request.POST.get('contrato')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        activo        = request.POST.get('activo')     # '1' o '0'

        # =========================================================
        # OBTENER OBJETOS RELACIONADOS
        # =========================================================

        persona_obj = Persona.objects.get(
            pk=persona_id
        )

        puesto_obj = Puesto.objects.get(
            pk=puesto_id
        )

        contrato_obj = Contrato.objects.get(
            pk=contrato_id
        )

        activo_bool = activo == '1'

        # =========================================================
        # CREAR EMPLEADO
        # =========================================================

        if accion == 'crear' or not accion:

            Empleado.objects.create(

                idPersona=persona_obj,

                idPuesto=puesto_obj,

                idContrato=contrato_obj,

                Fecha_Ingreso=fecha_ingreso,

                Activo=activo_bool,
            )

        # =========================================================
        # MODIFICAR EMPLEADO
        # =========================================================

        elif accion == 'modificar' and empleado_id:

            empleado = Empleado.objects.get(
                pk=empleado_id
            )

            empleado.idPersona = persona_obj

            empleado.idPuesto = puesto_obj

            empleado.idContrato = contrato_obj

            empleado.Fecha_Ingreso = fecha_ingreso

            empleado.Activo = activo_bool

            empleado.save()

        # =========================================================
        # PATRÓN PRG
        # Evita reenviar el formulario al recargar la página
        # =========================================================

        return redirect('empleados')

    # =========================================================
    # GET: MOSTRAR FORMULARIO + TABLA
    # =========================================================

    return render(
        request,
        'empleados.html',
        {

            'personas':
                Persona.objects.order_by(
                    'Nombre_Completo'
                ),

            'puestos':
                Puesto.objects.select_related(
                    'idDepartamento'
                ).order_by(
                    'Nombre'
                ),

            'contratos':
                Contrato.objects.all(),

            'empleados':
                Empleado.objects.select_related(
                    'idPersona',
                    'idPuesto',
                    'idContrato'
                ).order_by(
                    'idPersona__Nombre_Completo'
                ),
        }
    )


# =========================================================
# Vista: Editar Empleado
# Carga el formulario con los datos del empleado seleccionado
# =========================================================
@requiere_permiso("empleados", "editar")
def editar_empleado(request, id_empleado):

    # =========================================================
    # OBTENER EL EMPLEADO A MODIFICAR
    # =========================================================

    empleado = get_object_or_404(
        Empleado,
        pk=id_empleado
    )

    # =========================================================
    # SI PRESIONA GUARDAR CAMBIOS
    # =========================================================

    if request.method == 'POST':

        empleado.idPersona = Persona.objects.get(
            pk=request.POST.get('persona')
        )

        empleado.idPuesto = Puesto.objects.get(
            pk=request.POST.get('puesto')
        )

        empleado.idContrato = Contrato.objects.get(
            pk=request.POST.get('contrato')
        )

        empleado.Fecha_Ingreso = request.POST.get(
            'fecha_ingreso'
        )

        empleado.Activo = (
            request.POST.get('activo') == '1'
        )

        empleado.save()

        return redirect(
            'empleados'
        )

    # =========================================================
    # GET: PRE-RELLENAR FORMULARIO CON LOS DATOS ACTUALES
    # =========================================================

    return render(
        request,
        'empleados.html',
        {

            'empleado_editar':
                empleado,

            'personas':
                Persona.objects.order_by(
                    'Nombre_Completo'
                ),

            'puestos':
                Puesto.objects.select_related(
                    'idDepartamento'
                ).order_by(
                    'Nombre'
                ),

            'contratos':
                Contrato.objects.all(),

            'empleados':
                Empleado.objects.select_related(
                    'idPersona',
                    'idPuesto',
                    'idContrato'
                ).order_by(
                    'idPersona__Nombre_Completo'
                ),
        }
    )


# =========================================================
# Vista: Eliminar Empleado
# =========================================================
@requiere_permiso("empleados", "eliminar")
def eliminar_empleado(request, id_empleado):

    empleado = get_object_or_404(
        Empleado,
        pk=id_empleado
    )

    empleado.delete()

    return redirect(
        'empleados'
    )



# =========================================================
# Vista: Pasantes — registro, modificación y listado
# =========================================================
@requiere_permiso("empleados", "ver")
def registrar_pasante(request):

    # ── POST: crear o modificar ────────────────────────────
    if request.method == 'POST':

        accion     = request.POST.get('accion')       # 'crear' o 'modificar'
        pasante_id = request.POST.get('pasante_id')   # vacío si es nuevo

        # =========================================================
        # BLOQUEAR SEGÚN LA ACCIÓN
        # =========================================================

        if accion == 'modificar':

            bloqueo = bloquear_si_no_puede(
                request,
                "empleados",
                "editar"
            )

        else:

            bloqueo = bloquear_si_no_puede(
                request,
                "empleados",
                "crear"
            )

        # Si el usuario no tiene permiso, se detiene la operación
        if bloqueo:
            return bloqueo

        # =========================================================
        # OBTENER DATOS DEL FORMULARIO
        # =========================================================

        persona_id    = request.POST.get('persona')
        puesto_id     = request.POST.get('puesto')
        supervisor_id = request.POST.get('empleado_sup')
        fecha_inicio  = request.POST.get('fecha_inicio')
        fecha_fin     = request.POST.get('fecha_fin') or None
        universidad   = request.POST.get('universidad')
        carrera       = request.POST.get('carrera')
        tutor_univ    = request.POST.get('tutor_universitario')
        activo        = request.POST.get('activo')       # '1' o '0'

        # =========================================================
        # OBTENER OBJETOS RELACIONADOS
        # =========================================================

        persona_obj = Persona.objects.get(
            pk=persona_id
        )

        puesto_obj = Puesto.objects.get(
            pk=puesto_id
        )

        supervisor_obj = Empleado.objects.get(
            pk=supervisor_id
        )

        activo_bool = activo == '1'

        # =========================================================
        # CREAR PASANTE
        # =========================================================

        if accion == 'crear' or not accion:

            Pasante.objects.create(

                idPersona=persona_obj,

                idPuesto=puesto_obj,

                idEmpleado_Sup=supervisor_obj,

                Fecha_Inicio=fecha_inicio,

                Fecha_Fin=fecha_fin,

                # Se mantiene el nombre exacto de tu modelo
                Univercidad=universidad,

                Carrera=carrera,

                # Se mantiene el nombre exacto de tu modelo
                Tutor_Univercitario=tutor_univ,

                Activo=activo_bool,
            )

        # =========================================================
        # MODIFICAR PASANTE
        # =========================================================

        elif accion == 'modificar' and pasante_id:

            pasante = Pasante.objects.get(
                pk=pasante_id
            )

            pasante.idPersona = persona_obj

            pasante.idPuesto = puesto_obj

            pasante.idEmpleado_Sup = supervisor_obj

            pasante.Fecha_Inicio = fecha_inicio

            pasante.Fecha_Fin = fecha_fin

            pasante.Univercidad = universidad

            pasante.Carrera = carrera

            pasante.Tutor_Univercitario = tutor_univ

            pasante.Activo = activo_bool

            pasante.save()

        # =========================================================
        # PATRÓN PRG
        # Evita reenviar el formulario al recargar
        # =========================================================

        return redirect(
            'pasantes'
        )

    # =========================================================
    # GET: MOSTRAR FORMULARIO + TABLA
    # =========================================================

    return render(
        request,
        'pasantes.html',
        {

            'personas':
                Persona.objects.order_by(
                    'Nombre_Completo'
                ),

            'puestos':
                Puesto.objects.order_by(
                    'Nombre'
                ),

            # =====================================================
            # OBTENCIÓN DE SUPERVISORES
            # Trae los empleados y su persona relacionada
            # =====================================================

            'supervisores':
                Empleado.objects.select_related(
                    'idPersona'
                ).order_by(
                    'idPersona__Nombre_Completo'
                ),

            # =====================================================
            # LISTADO DE PASANTES
            # Optimizado con select_related para evitar N+1
            # =====================================================

            'pasantes':
                Pasante.objects.select_related(
                    'idPersona',
                    'idPuesto',
                    'idEmpleado_Sup__idPersona'
                ).order_by(
                    'idPersona__Nombre_Completo'
                ),
        }
    )


# =========================================================
# Vista: Editar Pasante
# Carga el formulario con los datos del pasante seleccionado
# =========================================================
@requiere_permiso("empleados", "editar")
def editar_pasante(request, id_pasante):

    # =========================================================
    # OBTENER EL PASANTE A MODIFICAR
    # =========================================================

    pasante = get_object_or_404(
        Pasante,
        pk=id_pasante
    )

    # =========================================================
    # SI PRESIONA GUARDAR CAMBIOS
    # =========================================================

    if request.method == 'POST':

        pasante.idPersona = Persona.objects.get(
            pk=request.POST.get('persona')
        )

        pasante.idPuesto = Puesto.objects.get(
            pk=request.POST.get('puesto')
        )

        pasante.idEmpleado_Sup = Empleado.objects.get(
            pk=request.POST.get('empleado_sup')
        )

        pasante.Fecha_Inicio = request.POST.get(
            'fecha_inicio'
        )

        pasante.Fecha_Fin = (
            request.POST.get('fecha_fin')
            or None
        )

        pasante.Univercidad = request.POST.get(
            'universidad'
        )

        pasante.Carrera = request.POST.get(
            'carrera'
        )

        pasante.Tutor_Univercitario = request.POST.get(
            'tutor_universitario'
        )

        pasante.Activo = (
            request.POST.get('activo') == '1'
        )

        pasante.save()

        return redirect(
            'pasantes'
        )

    # =========================================================
    # GET: PRE-RELLENAR FORMULARIO
    # =========================================================

    return render(
        request,
        'pasantes.html',
        {

            'pasante_editar':
                pasante,

            'personas':
                Persona.objects.order_by(
                    'Nombre_Completo'
                ),

            'puestos':
                Puesto.objects.order_by(
                    'Nombre'
                ),

            'supervisores':
                Empleado.objects.select_related(
                    'idPersona'
                ).order_by(
                    'idPersona__Nombre_Completo'
                ),

            'pasantes':
                Pasante.objects.select_related(
                    'idPersona',
                    'idPuesto',
                    'idEmpleado_Sup__idPersona'
                ).order_by(
                    'idPersona__Nombre_Completo'
                ),
        }
    )



# =========================================================
# Vista: Salarios — registro, modificación y listado
# =========================================================
@requiere_permiso("empleados", "ver")
def registrar_salario(request):

    # =========================================================
    # POST: CREAR O MODIFICAR
    # =========================================================
    if request.method == 'POST':

        accion = request.POST.get(
            'accion'
        )

        salario_id = request.POST.get(
            'salario_id'
        )

        # =========================================================
        # BLOQUEAR SEGÚN LA ACCIÓN
        # =========================================================

        if accion == 'modificar':

            bloqueo = bloquear_si_no_puede(
                request,
                "empleados",
                "editar"
            )

        else:

            bloqueo = bloquear_si_no_puede(
                request,
                "empleados",
                "crear"
            )

        # Si el usuario no tiene permiso, se detiene la operación
        if bloqueo:
            return bloqueo

        # =========================================================
        # OBTENER DATOS DEL FORMULARIO
        # =========================================================

        empleado_id = request.POST.get(
            'empleado'
        )

        fecha_inicio = request.POST.get(
            'fecha_inicio'
        )

        fecha_fin = request.POST.get(
            'fecha_fin'
        )

        salario_bruto = Decimal(
            request.POST.get(
                'salario_bruto'
            ) or 0
        )

        salario_sem_neto = Decimal(
            request.POST.get(
                'salario_sem_neto'
            ) or 0
        )

        comision = Decimal(
            request.POST.get(
                'comision_base'
            ) or 0
        )

        variable = Decimal(
            request.POST.get(
                'variable_base'
            ) or 0
        )

        viaticos = Decimal(
            request.POST.get(
                'viaticos_alimenticios'
            ) or 0
        )

        kilometraje = Decimal(
            request.POST.get(
                'kilometraje_base'
            ) or 0
        )

        bono = Decimal(
            request.POST.get(
                'bono_base'
            ) or 0
        )

        observaciones = request.POST.get(
            'observaciones'
        )

        # =========================================================
        # OBTENER EMPLEADO RELACIONADO
        # =========================================================

        empleado_obj = Empleado.objects.get(
            pk=empleado_id
        )

        # =========================================================
        # CREAR SALARIO
        # =========================================================

        if accion == 'crear' or not accion:

            SalarioEmpleado.objects.create(

                idEmpleado=empleado_obj,

                Fecha_Inicio=fecha_inicio,

                Fecha_Fin=(
                    fecha_fin
                    if fecha_fin
                    else None
                ),

                Salario_Bruto=salario_bruto,

                Salario_Sem_Neto=salario_sem_neto,

                Comision_Base=comision,

                Variable_Base=variable,

                Viaticos_Alimenticios=viaticos,

                Kilometraje_Base=kilometraje,

                Bono_Base=bono,

                Observaciones=observaciones
            )

        # =========================================================
        # MODIFICAR SALARIO
        # =========================================================

        elif accion == 'modificar' and salario_id:

            salario = SalarioEmpleado.objects.get(
                pk=salario_id
            )

            salario.idEmpleado = empleado_obj

            salario.Fecha_Inicio = fecha_inicio

            salario.Fecha_Fin = (
                fecha_fin
                if fecha_fin
                else None
            )

            salario.Salario_Bruto = salario_bruto

            salario.Salario_Sem_Neto = salario_sem_neto

            salario.Comision_Base = comision

            salario.Variable_Base = variable

            salario.Viaticos_Alimenticios = viaticos

            salario.Kilometraje_Base = kilometraje

            salario.Bono_Base = bono

            salario.Observaciones = observaciones

            salario.save()

        # =========================================================
        # PATRÓN PRG
        # Evita reenviar el formulario al recargar
        # =========================================================

        return redirect(
            'salarios'
        )

    # =========================================================
    # GET: MOSTRAR FORMULARIO + TABLA
    # =========================================================

    return render(
        request,
        'salario.html',
        {

            # =====================================================
            # EMPLEADOS ACTIVOS
            # =====================================================

            'empleados':
                Empleado.objects.select_related(
                    'idPersona',
                    'idPuesto'
                ).filter(
                    Activo=True
                ).order_by(
                    'idPersona__Nombre_Completo'
                ),

            # =====================================================
            # LISTADO DE SALARIOS
            # =====================================================

            'salarios':
                SalarioEmpleado.objects.select_related(
                    'idEmpleado',
                    'idEmpleado__idPersona',
                    'idEmpleado__idPuesto'
                ).order_by(
                    '-Fecha_Inicio'
                ),

            'salario_editar':
                None
        }
    )


# =========================================================
# Vista: Editar Salario
# Carga el formulario con los datos del salario seleccionado
# =========================================================
@requiere_permiso("empleados", "editar")
def editar_salario(request, id_salario):

    # =========================================================
    # OBTENER EL SALARIO A MODIFICAR
    # =========================================================

    salario = get_object_or_404(
        SalarioEmpleado,
        pk=id_salario
    )

    # =========================================================
    # SI PRESIONA GUARDAR CAMBIOS
    # =========================================================

    if request.method == 'POST':

        salario.idEmpleado = Empleado.objects.get(
            pk=request.POST.get(
                'empleado'
            )
        )

        salario.Fecha_Inicio = request.POST.get(
            'fecha_inicio'
        )

        salario.Fecha_Fin = (
            request.POST.get(
                'fecha_fin'
            )
            or None
        )

        salario.Salario_Bruto = Decimal(
            request.POST.get(
                'salario_bruto'
            )
            or 0
        )

        salario.Salario_Sem_Neto = Decimal(
            request.POST.get(
                'salario_sem_neto'
            )
            or 0
        )

        salario.Comision_Base = Decimal(
            request.POST.get(
                'comision_base'
            )
            or 0
        )

        salario.Variable_Base = Decimal(
            request.POST.get(
                'variable_base'
            )
            or 0
        )

        salario.Viaticos_Alimenticios = Decimal(
            request.POST.get(
                'viaticos_alimenticios'
            )
            or 0
        )

        salario.Kilometraje_Base = Decimal(
            request.POST.get(
                'kilometraje_base'
            )
            or 0
        )

        salario.Bono_Base = Decimal(
            request.POST.get(
                'bono_base'
            )
            or 0
        )

        salario.Observaciones = request.POST.get(
            'observaciones'
        )

        salario.save()

        return redirect(
            'salarios'
        )

    # =========================================================
    # GET: PRE-RELLENAR FORMULARIO
    # =========================================================

    return render(
        request,
        'salario.html',
        {

            'salario_editar':
                salario,

            'empleados':
                Empleado.objects.select_related(
                    'idPersona',
                    'idPuesto'
                ).filter(
                    Activo=True
                ).order_by(
                    'idPersona__Nombre_Completo'
                ),

            'salarios':
                SalarioEmpleado.objects.select_related(
                    'idEmpleado',
                    'idEmpleado__idPersona',
                    'idEmpleado__idPuesto'
                ).order_by(
                    '-Fecha_Inicio'
                )
        }
    )



# =========================================================
# Vista: Salarios — registro, modificación y listado
# =========================================================
@requiere_permiso("salarios", "ver")
def registrar_salario(request):

    if request.method == 'POST':

        accion = request.POST.get('accion')
        salario_id = request.POST.get('salario_id')

        # =====================================================
        # BLOQUEAR SEGÚN LA ACCIÓN
        # =====================================================
        if accion == 'modificar':
            bloqueo = bloquear_si_no_puede(
                request,
                "salarios",
                "editar"
            )
        else:
            bloqueo = bloquear_si_no_puede(
                request,
                "salarios",
                "crear"
            )

        if bloqueo:
            return bloqueo

        # =====================================================
        # DATOS DEL FORMULARIO
        # =====================================================
        empleado_id = request.POST.get('empleado')

        fecha_inicio = request.POST.get(
            'fecha_inicio'
        )

        fecha_fin = request.POST.get(
            'fecha_fin'
        )

        salario_bruto = Decimal(
            request.POST.get('salario_bruto') or 0
        )

        salario_sem_neto = Decimal(
            request.POST.get('salario_sem_neto') or 0
        )

        comision = Decimal(
            request.POST.get('comision_base') or 0
        )

        variable = Decimal(
            request.POST.get('variable_base') or 0
        )

        viaticos = Decimal(
            request.POST.get('viaticos_alimenticios') or 0
        )

        kilometraje = Decimal(
            request.POST.get('kilometraje_base') or 0
        )

        bono = Decimal(
            request.POST.get('bono_base') or 0
        )

        observaciones = request.POST.get(
            'observaciones'
        )

        # =====================================================
        # OBTENER EMPLEADO
        # =====================================================
        empleado_obj = Empleado.objects.get(
            pk=empleado_id
        )

        # =====================================================
        # CREAR SALARIO
        # =====================================================
        if accion == 'crear' or not accion:

            SalarioEmpleado.objects.create(

                idEmpleado=empleado_obj,

                Fecha_Inicio=fecha_inicio,

                Fecha_Fin=(
                    fecha_fin
                    if fecha_fin
                    else None
                ),

                Salario_Bruto=salario_bruto,

                Salario_Sem_Neto=salario_sem_neto,

                Comision_Base=comision,

                Variable_Base=variable,

                Viaticos_Alimenticios=viaticos,

                Kilometraje_Base=kilometraje,

                Bono_Base=bono,

                Observaciones=observaciones
            )

        # =====================================================
        # MODIFICAR SALARIO
        # =====================================================
        elif accion == 'modificar' and salario_id:

            salario = get_object_or_404(
                SalarioEmpleado,
                pk=salario_id
            )

            salario.idEmpleado = empleado_obj

            salario.Fecha_Inicio = fecha_inicio

            salario.Fecha_Fin = (
                fecha_fin
                if fecha_fin
                else None
            )

            salario.Salario_Bruto = salario_bruto

            salario.Salario_Sem_Neto = salario_sem_neto

            salario.Comision_Base = comision

            salario.Variable_Base = variable

            salario.Viaticos_Alimenticios = viaticos

            salario.Kilometraje_Base = kilometraje

            salario.Bono_Base = bono

            salario.Observaciones = observaciones

            salario.save()

        # =====================================================
        # PATRÓN PRG
        # =====================================================
        return redirect('salarios')

    # =========================================================
    # GET: MOSTRAR FORMULARIO + LISTADO
    # =========================================================
    return render(
        request,
        'salario.html',
        {

            'empleados': Empleado.objects.select_related(
                'idPersona',
                'idPuesto'
            ).filter(
                Activo=True
            ).order_by(
                'idPersona__Nombre_Completo'
            ),

            'salarios': SalarioEmpleado.objects.select_related(
                'idEmpleado',
                'idEmpleado__idPersona',
                'idEmpleado__idPuesto'
            ).order_by(
                '-Fecha_Inicio'
            ),

            'salario_editar': None
        }
    )


# =========================================================
# Vista: Editar Salario
# Carga el formulario con los datos del salario seleccionado
# =========================================================
@requiere_permiso("salarios", "editar")
def editar_salario(request, id_salario):

    salario = get_object_or_404(
        SalarioEmpleado,
        pk=id_salario
    )

    # =====================================================
    # SI SE ENVÍA EL FORMULARIO DESDE LA VISTA DE EDICIÓN
    # =====================================================
    if request.method == 'POST':

        # -------------------------------------------------
        # Verificar nuevamente el permiso de edición
        # -------------------------------------------------
        bloqueo = bloquear_si_no_puede(
            request,
            "salarios",
            "editar"
        )

        if bloqueo:
            return bloqueo

        # -------------------------------------------------
        # Actualizar información
        # -------------------------------------------------
        salario.idEmpleado = Empleado.objects.get(
            pk=request.POST.get('empleado')
        )

        salario.Fecha_Inicio = request.POST.get(
            'fecha_inicio'
        )

        fecha_fin = request.POST.get(
            'fecha_fin'
        )

        salario.Fecha_Fin = (
            fecha_fin
            if fecha_fin
            else None
        )

        salario.Salario_Bruto = Decimal(
            request.POST.get('salario_bruto') or 0
        )

        salario.Salario_Sem_Neto = Decimal(
            request.POST.get('salario_sem_neto') or 0
        )

        salario.Comision_Base = Decimal(
            request.POST.get('comision_base') or 0
        )

        salario.Variable_Base = Decimal(
            request.POST.get('variable_base') or 0
        )

        salario.Viaticos_Alimenticios = Decimal(
            request.POST.get('viaticos_alimenticios') or 0
        )

        salario.Kilometraje_Base = Decimal(
            request.POST.get('kilometraje_base') or 0
        )

        salario.Bono_Base = Decimal(
            request.POST.get('bono_base') or 0
        )

        salario.Observaciones = request.POST.get(
            'observaciones'
        )

        salario.save()

        return redirect('salarios')

    # =====================================================
    # GET: MOSTRAR FORMULARIO DE EDICIÓN
    # =====================================================
    return render(
        request,
        'salario.html',
        {

            'salario_editar': salario,

            'empleados': Empleado.objects.select_related(
                'idPersona',
                'idPuesto'
            ).filter(
                Activo=True
            ).order_by(
                'idPersona__Nombre_Completo'
            ),

            'salarios': SalarioEmpleado.objects.select_related(
                'idEmpleado',
                'idEmpleado__idPersona',
                'idEmpleado__idPuesto'
            ).order_by(
                '-Fecha_Inicio'
            )
        }
    )


# =========================================================
# Obtener compensación base según el puesto del empleado
# =========================================================
@requiere_permiso("salarios", "ver")
def obtener_compensacion_empleado(
    request,
    id_empleado
):

    try:

        empleado = Empleado.objects.select_related(
            'idPuesto'
        ).get(
            pk=id_empleado
        )

        print(
            "EMPLEADO:",
            empleado
        )

        print(
            "PUESTO:",
            empleado.idPuesto
        )

        print(
            "ID PUESTO:",
            empleado.idPuesto.idPuesto
        )

        compensaciones = Compensacion_Puesto.objects.filter(
            idPuesto=empleado.idPuesto
        )

        print(
            "COMPENSACIONES ENCONTRADAS:",
            compensaciones.count()
        )

        compensacion = compensaciones.order_by(
            '-Vigencia'
        ).first()

        # =====================================================
        # NO EXISTE COMPENSACIÓN
        # =====================================================
        if compensacion is None:

            return JsonResponse({

                'success': False,

                'mensaje':
                    'El puesto no tiene compensación configurada.'
            })

        # =====================================================
        # DEVOLVER COMPENSACIÓN
        # =====================================================
        return JsonResponse({

            'success': True,

            'id_puesto':
                empleado.idPuesto.idPuesto,

            'puesto':
                empleado.idPuesto.Nombre,

            'salario_bruto':
                float(
                    compensacion.Salario_Bruto
                ),

            'salario_sem_neto':
                float(
                    compensacion.Salario_Sem_Neto
                ),

            'comision_base':
                float(
                    compensacion.Comision_Base
                ),

            'variable_base':
                float(
                    compensacion.Variable_Base
                ),

            'viaticos_alimenticios':
                float(
                    compensacion.Viaticos_Alimenticios
                ),

            'kilometraje_base':
                float(
                    compensacion.Kilometraje_Base
                ),

            'bono_base':
                float(
                    compensacion.Bono_Base
                ),

            'vigencia':
                compensacion.Vigencia.strftime(
                    '%Y-%m-%d'
                )
                if compensacion.Vigencia
                else None

        })

    # =====================================================
    # EMPLEADO NO ENCONTRADO
    # =====================================================
    except Empleado.DoesNotExist:

        return JsonResponse({

            'success': False,

            'mensaje':
                'Empleado no encontrado.'
        })

    # =====================================================
    # ERROR GENERAL
    # =====================================================
    except Exception as e:

        return JsonResponse({

            'success': False,

            'mensaje':
                str(e)
        })




def reclutamiento_view(request):
    return render(request, 'reclutamiento.html')

@requiere_permiso("reclutamiento", "ver")
def registrar_vacante(request):

    if request.method == 'POST':

        accion = request.POST.get('accion')
        vacante_asig_id = request.POST.get('vacante_asig_id')

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN LA ACCIÓN
        # ─────────────────────────────────────────────
        if accion == 'modificar':
            bloqueo = bloquear_si_no_puede(request, "reclutamiento", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "reclutamiento", "crear")

        if bloqueo:
            return bloqueo

        # =====================================================
        # DATOS DE VACANTE
        # =====================================================
        fecha_registro = request.POST.get('fecha_registro')
        titulo = request.POST.get('titulo_publicacion')
        motivo = request.POST.get('motivo')
        experiencia = request.POST.get('experiencia_requerida')
        salario_bruto = request.POST.get('salario_bruto')
        compensacion_total = request.POST.get('compensacion_total')
        cierre = request.POST.get('cierre_proceso')

        # =====================================================
        # RELACIONES
        # =====================================================
        estatus_id = request.POST.get('estatus')

        empleado_aut_id = request.POST.get('empleado_aut')
        empleado_eval_id = request.POST.get('empleado_eval')
        empleado_jefe_id = request.POST.get('empleado_jefe')
        empleado_sus_id = request.POST.get('empleado_sus')
        puesto_id = request.POST.get('puesto')

        # =====================================================
        # CREAR
        # =====================================================

        print("SALARIO BRUTO:", salario_bruto)
        print("COMPENSACION TOTAL:", compensacion_total)
        
        if accion == 'crear':

            vacante = Vacante.objects.create(

                Fecha_Registro=fecha_registro,
                TituloPublicacion=titulo,
                Motivo=motivo,
                Expe_Requerida=experiencia,
                Salario_Bruto=salario_bruto,
                Compensacion_Total=compensacion_total,
                Cierre_Proceso=cierre if cierre else None
            )

            Vacante_Asig.objects.create(

                id_Vacante=vacante,

                id_Estatus_Vacante_id=estatus_id,

                idEmpleado_Aut_id=empleado_aut_id,

                idEmpleado_Rel_Ev_id=empleado_eval_id,

                idEmpleado_Jef_Puest_id=empleado_jefe_id,

                idEmpleado_Sus_id=(
                    empleado_sus_id
                    if empleado_sus_id else None
                ),

                idPuesto_id=puesto_id
            )

        # =====================================================
        # MODIFICAR
        # =====================================================
        elif accion == 'modificar':

            asignacion = get_object_or_404(
                Vacante_Asig,
                pk=vacante_asig_id
            )

            # Obtener la vacante asociada
            vacante = asignacion.id_Vacante

            vacante.Fecha_Registro = fecha_registro
            vacante.TituloPublicacion = titulo
            vacante.Motivo = motivo
            vacante.Expe_Requerida = experiencia

            vacante.Salario_Bruto = salario_bruto
            vacante.Compensacion_Total = compensacion_total

            vacante.Cierre_Proceso = (
                cierre if cierre else None
            )

            vacante.save()

            asignacion.id_Estatus_Vacante_id = estatus_id
            asignacion.idEmpleado_Aut_id = empleado_aut_id
            asignacion.idEmpleado_Rel_Ev_id = empleado_eval_id
            asignacion.idEmpleado_Jef_Puest_id = empleado_jefe_id

            asignacion.idEmpleado_Sus_id = (
                empleado_sus_id if empleado_sus_id else None
            )

            asignacion.idPuesto_id = puesto_id

            asignacion.save()

        return redirect('vacantes')
    
    

    # =========================================================
    # CARGA INICIAL DE PANTALLA
    # =========================================================
    return render(
        request,
        'vacante.html',
        {

            'vacante_editar': None,

            'estatuses': Estatus.objects.all(),

            'empleados': Empleado.objects.select_related(
                'idPersona'
            ),

            'puestos': Puesto.objects.all(),

            'vacantes': Vacante_Asig.objects.select_related(
                'id_Vacante',
                'id_Estatus_Vacante',
                'idPuesto',
                'idEmpleado_Aut__idPersona',
                'idEmpleado_Rel_Ev__idPersona',
                'idEmpleado_Jef_Puest__idPersona',
                'idEmpleado_Sus__idPersona'
            )
        }
    )


@requiere_permiso("reclutamiento", "editar")
def editar_vacante(request, id_vacante_asig):

    vacante = get_object_or_404(
        Vacante_Asig,
        pk=id_vacante_asig
    )

    return render(
        request,
        'vacante.html',
        {

            'vacante_editar': vacante,

            'estatuses': Estatus.objects.all(),

            'empleados': Empleado.objects.select_related(
                'idPersona'
            ),

            'puestos': Puesto.objects.all(),

            'vacantes': Vacante_Asig.objects.select_related(
                'id_Vacante',
                'id_Estatus_Vacante',
                'idPuesto',
                'idEmpleado_Aut__idPersona',
                'idEmpleado_Rel_Ev__idPersona',
                'idEmpleado_Jef_Puest__idPersona',
                'idEmpleado_Sus__idPersona'
            )
        }
    )

def obtener_compensacion_puesto(request, id_puesto):

    try:

        puesto = Puesto.objects.get(
            pk=id_puesto
        )

        compensacion = Compensacion_Puesto.objects.filter(
            idPuesto=puesto
        ).first()

        if compensacion is None:

            return JsonResponse({
                'success': False,
                'mensaje': 'No existe compensación configurada.'
            })

        compensacion_total = (

            compensacion.Salario_Bruto +

            compensacion.Comision_Base +

            compensacion.Variable_Base +

            compensacion.Viaticos_Alimenticios +

            compensacion.Kilometraje_Base +

            compensacion.Bono_Base
        )

        return JsonResponse({

            'success': True,

            'salario_bruto':
                float(compensacion.Salario_Bruto),

            'compensacion_total':
                float(compensacion_total)
        })

    except Exception as e:

        return JsonResponse({

            'success': False,

            'mensaje': str(e)
        })



# =========================================================
# Registrar y Modificar Reclutamiento de personal par ala vacante abierta
# =========================================================
@requiere_permiso("reclutamiento", "ver")
def registrar_candidato(request):

    if request.method == 'POST':

        accion = request.POST.get('accion')
        candidato_id = request.POST.get('candidato_id')

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN LA ACCIÓN
        # ─────────────────────────────────────────────
        if accion == 'modificar':
            bloqueo = bloquear_si_no_puede(request, "reclutamiento", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "reclutamiento", "crear")

        if bloqueo:
            return bloqueo

        if accion == 'crear':

            Vacante_Candidato.objects.create(
                Activo=request.POST.get('activo') == '1',
                Observaciones=request.POST.get('observaciones'),
                id_Vacante_id=request.POST.get('vacante'),
                idPersona_id=request.POST.get('persona'),
                id_Fase_id=request.POST.get('fase'),
                id_Proceso_id=request.POST.get('proceso')
            )

        elif accion == 'modificar':

            candidato = get_object_or_404(
                Vacante_Candidato,
                pk=candidato_id
            )

            candidato.Activo = request.POST.get('activo') == '1'
            candidato.Observaciones = request.POST.get('observaciones')
            candidato.id_Vacante_id = request.POST.get('vacante')
            candidato.idPersona_id = request.POST.get('persona')
            candidato.id_Fase_id = request.POST.get('fase')
            candidato.id_Proceso_id = request.POST.get('proceso')

            candidato.save()

        return redirect('candidatos')

    # ESTE BLOQUE ES NECESARIO PARA LAS PETICIONES GET
    contexto = {

        'candidato_editar': None,

        'personas': Persona.objects.all(),

        'vacantes': Vacante.objects.all(),

        'fases': FaseCandidato.objects.all(),

        'procesos': ProcesoFase.objects.all(),

        'candidatos': Vacante_Candidato.objects.select_related(
            'idPersona',
            'id_Vacante',
            'id_Fase',
            'id_Proceso'
        )
    }

    return render(
        request,
        'reclut_Vacante.html',
        contexto
    )


@requiere_permiso("reclutamiento", "editar")
def editar_candidato(request,id):

    candidato = get_object_or_404(
        Vacante_Candidato,
        pk=id
    )

    contexto = {

        'candidato_editar': candidato,

        'personas': Persona.objects.all(),

        'vacantes': Vacante.objects.all(),

        'fases': FaseCandidato.objects.all(),

        'procesos': ProcesoFase.objects.all(),

        'candidatos': Vacante_Candidato.objects.select_related(
            'idPersona',
            'id_Vacante',
            'id_Fase',
            'id_Proceso'
        )
    }

    return render(
        request,
        'reclut_Vacante.html',
        contexto
    )



def vacaciones_view(request):
    return render(request, 'vacaciones.html')


# =========================================================
# REGISTRAR Y MODIFICAR SOLICITUD DE VACACIONES
# =========================================================
@requiere_permiso("vacaciones", "ver")
def registrar_solicitud_vacacion(request):

    if request.method == 'POST':

        accion = request.POST.get('accion')

        solicitud_id = request.POST.get('solicitud_id')

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN LA ACCIÓN
        # ─────────────────────────────────────────────
        if accion == 'modificar':
            bloqueo = bloquear_si_no_puede(request, "vacaciones", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "vacaciones", "crear")

        if bloqueo:
            return bloqueo


        # ============================================
        # CREAR
        # ============================================

        if accion == 'crear':

            VacacionSolicitud.objects.create(

                Fecha_Solicitud=request.POST.get('fecha_solicitud'),

                Fecha_Inicio=request.POST.get('fecha_inicio'),

                Fecha_Fin=request.POST.get('fecha_fin'),

                Dias_Solicitud=request.POST.get('dias_solicitados'),

                id_Estatus_Vacante_id=request.POST.get('estado'),

                idEmpleado_Sol_Vac_id=request.POST.get('empleado'),

                idEmpleado_Respon_id=request.POST.get('aprobador')

            )


        # ============================================
        # MODIFICAR
        # ============================================

        elif accion == 'modificar':

            solicitud = get_object_or_404(
                VacacionSolicitud,
                pk=solicitud_id
            )

            solicitud.Fecha_Solicitud = request.POST.get(
                'fecha_solicitud'
            )

            solicitud.Fecha_Inicio = request.POST.get(
                'fecha_inicio'
            )

            solicitud.Fecha_Fin = request.POST.get(
                'fecha_fin'
            )

            solicitud.Dias_Solicitud = request.POST.get(
                'dias_solicitados'
            )

            solicitud.id_Estatus_Vacante_id = request.POST.get(
                'estado'
            )

            solicitud.idEmpleado_Sol_Vac_id = request.POST.get(
                'empleado'
            )

            solicitud.idEmpleado_Respon_id = request.POST.get(
                'aprobador'
            )

            solicitud.save()


        return redirect('solicitudes_vacaciones')


    # ============================================
    # GET
    # ============================================

    contexto = {

        'solicitud_editar': None,

        'empleados': Empleado.objects.all(),

        'aprobadores': Empleado.objects.all(),

        'estados': Estatus.objects.all(),

        'solicitudes': VacacionSolicitud.objects.select_related(

            'idEmpleado_Sol_Vac',

            'idEmpleado_Respon',

            'id_Estatus_Vacante'

        )

    }

    return render(

        request,

        'sol_Vacacion.html',

        contexto

    )


# =========================================================
# EDITAR SOLICITUD DE VACACIONES
# =========================================================
@requiere_permiso("vacaciones", "editar")
def editar_solicitud_vacacion(request, id):

    solicitud = get_object_or_404(

        VacacionSolicitud,

        pk=id

    )


    contexto = {

        'solicitud_editar': solicitud,

        'empleados': Empleado.objects.all(),

        'aprobadores': Empleado.objects.all(),

        'estados': Estatus.objects.all(),

        'solicitudes': VacacionSolicitud.objects.select_related(

            'idEmpleado_Sol_Vac',

            'idEmpleado_Respon',

            'id_Estatus_Vacante'

        )

    }


    return render(

        request,

        'sol_Vacacion.html',

        contexto

    )


from datetime import date
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect

# =========================================================
# GUARDAR SALDO DE VACACIONES (CON LÓGICA PROGRESIVA ACUMULADA)
# =========================================================
@requiere_permiso("vacaciones", "ver")
def guardar_saldo_vacaciones(request):

    if request.method == "POST":
        # 1. Validar permisos de creación
        bloqueo = bloquear_si_no_puede(request, "vacaciones", "crear")
        if bloqueo:
            return bloqueo

        empleado_id = request.POST.get("empleado")
        anio_param = request.POST.get("anio")

        if empleado_id:
            empleado = get_object_or_404(Empleado, idEmpleado=empleado_id)

            try:
                anio = int(anio_param) if anio_param else date.today().year
            except ValueError:
                anio = date.today().year

            hoy = date.today()
            fecha_corte = date(anio, 12, 31) if anio < hoy.year else hoy

            # 2. BUSCAR SALDO ANTERIOR DE ESTE EMPLEADO
            saldo_anterior = VacacionSaldo.objects.filter(
                idEmpleado_Sal_Vac=empleado,
                Anio__lt=anio
            ).order_by('-Anio').first()

            # 3. CÁLCULO DE DÍAS ACUMULADOS PROGRESIVO
            if saldo_anterior:
                disponibles_base = float(saldo_anterior.Dias_Disponibles or 0.0)
                inicio_periodo = date(anio, 1, 1)

                if fecha_corte > inicio_periodo:
                    dias_en_periodo = (fecha_corte - inicio_periodo).days
                    ganados_periodo = round((dias_en_periodo / 365.0) * 15, 2)
                else:
                    ganados_periodo = 0.0

                acumulados = round(disponibles_base + ganados_periodo, 2)
            else:
                fecha_ingreso = getattr(empleado, 'Fecha_Ingreso', None) or getattr(empleado, 'fecha_ingreso', None)
                if fecha_ingreso and fecha_corte > fecha_ingreso:
                    dias_trabajados = (fecha_corte - fecha_ingreso).days
                    acumulados = round((dias_trabajados / 365.0) * 15, 2)
                else:
                    acumulados = 0.0

            # 4. SOLICITUDES DE VACACIONES TOMADAS EN EL AÑO CONSULTADO
            solicitudes = VacacionSolicitud.objects.filter(
                idEmpleado_Sol_Vac=empleado,
                id_Estatus_Vacante__TipoEstatus__icontains="aprobad",
                Fecha_Inicio__year=anio
            )
            suma_tomados = solicitudes.aggregate(total=Sum('Dias_Solicitud'))['total']
            tomados = float(suma_tomados) if suma_tomados is not None else 0.0

            # 5. DÍAS DISPONIBLES FINALES
            disponibles = round(acumulados - tomados, 2)

            # 6. GUARDAR / ACTUALIZAR EN BASE DE DATOS
            saldo, creado = VacacionSaldo.objects.get_or_create(
                idEmpleado_Sal_Vac=empleado,
                Anio=anio
            )

            VacacionSaldo.objects.filter(pk=saldo.pk).update(
                Dias_Acumulados=acumulados,
                Dias_Tomado=tomados,
                Dias_Disponibles=disponibles
            )

    # Cargar datos actualizados para re-renderizar la tabla
    empleados = Empleado.objects.select_related('idPersona')
    saldos = VacacionSaldo.objects.select_related(
        'idEmpleado_Sal_Vac',
        'idEmpleado_Sal_Vac__idPersona'
    )

    contexto = {
        'empleados': empleados,
        'saldos': saldos,
        'saldo_editar': None
    }

    return render(request, 'con_Vacacion.html', contexto)

# =========================================================
# MODIFICAR CONSULTA DE VACACIONES
# =========================================================
@requiere_permiso("vacaciones", "editar")
def editar_saldo_vacaciones(request, id):

    saldo = get_object_or_404(
        VacacionSaldo,
        idSaldo=id
    )

    if request.method == "POST":

        # ==========================================
        # VALIDAR PERMISO PARA EDITAR
        # ==========================================
        bloqueo = bloquear_si_no_puede(
            request,
            "vacaciones",
            "editar"
        )

        if bloqueo:
            return bloqueo

        saldo.Anio = request.POST.get(
            "anio"
        )

        saldo.save()

    empleados = Empleado.objects.select_related(
        'idPersona'
    )

    saldos = VacacionSaldo.objects.select_related(
        'idEmpleado_Sal_Vac',
        'idEmpleado_Sal_Vac__idPersona'
    )

    return render(
        request,
        'con_Vacacion.html',
        {
            'empleados': empleados,

            'saldos': saldos,

            'saldo_editar': saldo
        }
    )


from datetime import date
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# =========================================================
# OBTENER EL SALDO DE VACACIONES (ACUMULATIVO SOBRE EL ÚLTIMO SALDO)
# =========================================================
@requiere_permiso("vacaciones", "ver")
def obtener_saldo_vacaciones(request):
    empleado_id = request.GET.get("empleado")
    anio_param = request.GET.get("anio")

    if not empleado_id:
        return JsonResponse({
            'acumulados': 0,
            'tomados': 0,
            'disponibles': 0
        })

    empleado = get_object_or_404(Empleado, idEmpleado=empleado_id)

    # 1. Obtener el año ingresado
    try:
        anio = int(anio_param) if anio_param else date.today().year
    except ValueError:
        anio = date.today().year

    hoy = date.today()
    fecha_corte = date(anio, 12, 31) if anio < hoy.year else hoy

    # 2. BUSCAR SI YA TIENE UN SALDO GUARDADO ANTERIOR A ESTE AÑO
    saldo_anterior = VacacionSaldo.objects.filter(
        idEmpleado_Sal_Vac=empleado,
        Anio__lt=anio  # Saldo de años menores al que estamos consultando
    ).order_by('-Anio').first()

    # 3. CÁLCULO DE DÍAS ACUMULADOS PROGRESIVO
    if saldo_anterior:
        # Puntos de partida: Los disponibles que le quedaron en el período anterior
        disponibles_base = float(saldo_anterior.Dias_Disponibles or 0.0)
        
        # Calculamos solo los días ganados desde el 1 de Enero del año consultado hasta la fecha de corte
        inicio_periodo = date(anio, 1, 1)
        if fecha_corte > inicio_periodo:
            dias_en_periodo = (fecha_corte - inicio_periodo).days
            ganados_periodo = round((dias_en_periodo / 365.0) * 15, 2)
        else:
            ganados_periodo = 0.0

        # Los acumulados para este nuevo período son: Lo que traía disponible + lo ganado en este período
        acumulados = round(disponibles_base + ganados_periodo, 2)

    else:
        # Si es la primera vez que se registra saldo para este empleado:
        fecha_ingreso = getattr(empleado, 'Fecha_Ingreso', None) or getattr(empleado, 'fecha_ingreso', None)
        if fecha_ingreso and fecha_corte > fecha_ingreso:
            dias_trabajados = (fecha_corte - fecha_ingreso).days
            acumulados = round((dias_trabajados / 365.0) * 15, 2)
        else:
            acumulados = 0.0

    # 4. SOLICITUDES DE VACACIONES TOMADAS EN EL AÑO CONSULTADO
    solicitudes = VacacionSolicitud.objects.filter(
        idEmpleado_Sol_Vac=empleado,
        id_Estatus_Vacante__TipoEstatus__icontains="aprobad",
        Fecha_Inicio__year=anio # Solo restamos lo tomado en ESTE período
    )

    resultado_tomados = solicitudes.aggregate(total=Sum('Dias_Solicitud'))['total']
    tomados = float(resultado_tomados) if resultado_tomados is not None else 0.0

    # 5. DÍAS DISPONIBLES FINALES
    disponibles = round(acumulados - tomados, 2)

    return JsonResponse({
        'acumulados': acumulados,
        'tomados': tomados,
        'disponibles': disponibles
    })

def elec_Asistencia_view(request):
    return render(request, 'elec_Asistencia.html')


# =========================================================
# GUARDAR ASISTENCIA
# =========================================================
@requiere_permiso("asistencia", "ver")
def guardar_asistencia(request):

    empleados = Empleado.objects.select_related(
        'idPersona'
    )

    estados = AsistenciaEstado.objects.all()

    if request.method == "POST":

        # ==========================================
        # VALIDAR PERMISO PARA CREAR
        # ==========================================
        bloqueo = bloquear_si_no_puede(
            request,
            "asistencia",
            "crear"
        )

        if bloqueo:
            return bloqueo

        empleado = Empleado.objects.get(
            idEmpleado=request.POST.get("empleado")
        )

        estado = AsistenciaEstado.objects.get(
            idAsis_Estado=request.POST.get("estado")
        )

        # Convertir string a objeto time
        hora_entrada = datetime.strptime(
            request.POST.get("hora_entrada"),
            "%H:%M"
        ).time()

        hora_salida = datetime.strptime(
            request.POST.get("hora_salida"),
            "%H:%M"
        ).time()

        asistencia = Asistencia(

            Fecha=request.POST.get("fecha"),

            Hora_Entrada=hora_entrada,

            Hora_Salida=hora_salida,

            idEmpleado=empleado,

            idAsis_Estado=estado

        )

        # El modelo calculará automáticamente Horas_Extra
        asistencia.save()

    asistencias = Asistencia.objects.select_related(

        'idEmpleado',

        'idEmpleado__idPersona',

        'idAsis_Estado'

    )

    return render(

        request,

        'asistencia.html',

        {

            'empleados': empleados,

            'estados': estados,

            'asistencias': asistencias

        }

    )


# =========================================================
# MODIFICAR ASISTENCIA
# =========================================================
@requiere_permiso("asistencia", "editar")
def editar_asistencia(request, id):

    asistencia = get_object_or_404(

        Asistencia,

        idAsistencia=id

    )

    if request.method == "POST":

        # ==========================================
        # VALIDAR PERMISO PARA EDITAR
        # ==========================================
        bloqueo = bloquear_si_no_puede(
            request,
            "asistencia",
            "editar"
        )

        if bloqueo:
            return bloqueo

        asistencia.Fecha = request.POST.get(
            "fecha"
        )

        asistencia.Hora_Entrada = datetime.strptime(
            request.POST.get(
                "hora_entrada"
            ),
            "%H:%M"
        ).time()

        asistencia.Hora_Salida = datetime.strptime(
            request.POST.get(
                "hora_salida"
            ),
            "%H:%M"
        ).time()

        empleado = Empleado.objects.get(

            idEmpleado=request.POST.get(
                "empleado"
            )

        )

        asistencia.idEmpleado = empleado

        estado = AsistenciaEstado.objects.get(

            idAsis_Estado=request.POST.get(
                "estado"
            )

        )

        asistencia.idAsis_Estado = estado

        # El modelo recalcula automáticamente las horas extra
        asistencia.save()

        return redirect(
            "asistencia"
        )

    empleados = Empleado.objects.select_related(

        'idPersona'

    )

    estados = AsistenciaEstado.objects.all()

    asistencias = Asistencia.objects.select_related(

        'idEmpleado',

        'idEmpleado__idPersona',

        'idAsis_Estado'

    )

    return render(

        request,

        'asistencia.html',

        {

            'empleados': empleados,

            'estados': estados,

            'asistencias': asistencias,

            'asistencia_editar': asistencia

        }

    )


# =========================================================
# GUARDAR PERMISO
# =========================================================
@requiere_permiso("permisos", "crear")
def guardar_permiso(request):

    # ==========================
    # EMPLEADOS
    # ==========================
    empleados = Empleado.objects.select_related(
        'idPersona'
    )

    # ==========================
    # TIPOS DE PERMISO
    # ==========================
    tipos_permiso = TipoPermiso.objects.all()

    # ==========================
    # SOLO ASISTENCIAS CON ESTADO "Permiso"
    # ==========================
    asistencias_permiso = Asistencia.objects.select_related(
        'idEmpleado',
        'idEmpleado__idPersona',
        'idAsis_Estado'
    ).filter(
        idAsis_Estado__TipoEstado='Permiso'
    )

    # ==========================
    # GUARDAR
    # ==========================
    if request.method == "POST":

        # ==========================================
        # VALIDAR PERMISO PARA CREAR
        # ==========================================
        bloqueo = bloquear_si_no_puede(
            request,
            "permisos",
            "crear"
        )

        if bloqueo:
            return bloqueo

        empleado = Empleado.objects.get(
            idEmpleado=request.POST.get("empleado")
        )

        asistencia = Asistencia.objects.get(
            idAsistencia=request.POST.get("asistencia")
        )

        tipo_permiso = TipoPermiso.objects.get(
            id_TipoPermiso=request.POST.get("tipo_permiso")
        )

        activo = request.POST.get("activo")

        permiso = Permiso(

            Activo=True if activo == "1" else False,

            Justificacion=request.POST.get(
                "justificacion"
            ),

            id_TipoPermiso=tipo_permiso,

            idAsistencia=asistencia,

            idEmpleado=empleado

        )

        permiso.save()

        return redirect(
            'guardar_permiso'
        )

    permisos = Permiso.objects.select_related(

        'idEmpleado',

        'idEmpleado__idPersona',

        'idAsistencia',

        'id_TipoPermiso'

    )

    return render(

        request,

        'permiso.html',

        {
            'empleados': empleados,
            'tipos_permiso': tipos_permiso,
            'asistencias_permiso': asistencias_permiso,
            'permisos': permisos
        }
    )



def accion_rotacion_view(request):
    return render(request, 'accion_rotacion.html')

# =========================================================
# GUARDAR DETALLE DE LA ACCIÓN DE PERSONAL
# =========================================================
@requiere_permiso("acciones_personal", "crear")
@transaction.atomic
def guardar_accion_tipo(request, id_accion):
    if request.method != "POST":
        return redirect("gestionar_accion")

    accion = get_object_or_404(AccionPersonal, pk=id_accion)
    tipo_accion = get_object_or_404(DetalleAccion, pk=request.POST.get("Tipo_Accion"))
    detalle = request.POST.get("Detalle")

    accion_tipo = AccionTipo(
        idAccion=accion,
        id_Detalle_Accion=tipo_accion,
        Detalle=detalle
    )

    # Ascenso / Ajuste Salarial
    if tipo_accion.Accion in ["Ascenso", "Ajuste Salarial"]:
        salario = get_object_or_404(SalarioEmpleado, pk=request.POST.get("idSalarioEmpleado"))
        nuevo_salario = Decimal(request.POST.get("nuevo_salario"))

        salario.Salario_Sem_Neto = nuevo_salario
        salario.save()

        accion_tipo.idSalarioEmpleado = salario
        accion_tipo.Monto_TA = nuevo_salario

    # Premio
    elif tipo_accion.Accion == "Premio":
        premio = get_object_or_404(PremioAsignado, pk=request.POST.get("idPremioAsignado"))
        accion_tipo.id_PremioAsignado = premio
        accion_tipo.Monto_TA = premio.Monto_Liquidado

    accion_tipo.save()

    messages.success(request, "La Acción de Personal fue registrada correctamente.")
    return redirect("accion_rotacion")


# =========================================================
# GUARDAR CABECERA DE LA ACCIÓN DEL PERSONAL
# =========================================================
@requiere_permiso("acciones_personal", "crear")
def registrar_cabecera_accion(request, pk=None):
    accion_cabecera = None
    paso_dos_habilitado = False

    if pk:
        accion_cabecera = get_object_or_404(AccionPersonal, pk=pk)
        paso_dos_habilitado = True

    if request.method == 'POST':
        action = request.POST.get('action')

        # GUARDAR CABECERA
        if action == 'guardar_cabecera':
            form_cabecera = AccionPersonalForm(request.POST)
            if form_cabecera.is_valid():
                nueva_cabecera = form_cabecera.save()
                messages.success(
                    request,
                    f"Cabecera guardada con éxito. Folio: {nueva_cabecera.idAccion}"
                )
                return redirect('gestionar_accion', pk=nueva_cabecera.idAccion)
            else:
                messages.error(request, "Error al validar los datos de la cabecera.")

        # FINALIZAR ACCIÓN
        elif action == 'finalizar_accion':
            id_cabecera_padre = request.POST.get('idAccion_padre')
            if not id_cabecera_padre:
                messages.error(request, "Error crítico: No se encontró la cabecera asociada al movimiento.")
                return redirect('crear_accion')

            cabecera_obj = get_object_or_404(AccionPersonal, pk=id_cabecera_padre)
            id_detalle_accion = request.POST.get('Tipo_Accion')
            id_salario_empleado = request.POST.get('idSalario')
            detalle_texto = request.POST.get('Detalle')

            if not id_detalle_accion or not detalle_texto:
                messages.error(request, "Por favor complete todos los campos requeridos de la especificación.")
                return redirect('gestionar_accion', pk=cabecera_obj.idAccion)

            try:
                catalogo_accion = get_object_or_404(DetalleAccion, pk=id_detalle_accion)
                
                salario_obj = None
                if id_salario_empleado:
                    salario_obj = get_object_or_404(SalarioEmpleado, pk=id_salario_empleado)

                premio_asignado = None
                id_premio_asignado = request.POST.get("idPremioAsignado")
                if id_premio_asignado:
                    premio_asignado = get_object_or_404(PremioAsignado, pk=id_premio_asignado)

                monto = None
                if catalogo_accion.Accion == "Premio":
                    monto = Decimal(request.POST.get("monto_premio"))
                elif catalogo_accion.Accion in ["Ascenso", "Ajuste Salarial"]:
                    monto = Decimal(request.POST.get("nuevo_salario"))
                    if salario_obj:
                        salario_obj.Salario_Sem_Neto = monto
                        salario_obj.save()

                AccionTipo.objects.create(
                    idAccion=cabecera_obj,
                    id_Detalle_Accion=catalogo_accion,
                    idSalarioEmpleado=salario_obj,
                    id_PremioAsignado=premio_asignado,
                    Monto_TA=monto,
                    Detalle=detalle_texto
                )

                messages.success(
                    request,
                    f"El movimiento administrativo del Folio {cabecera_obj.idAccion} se ha sellado y guardado correctamente."
                )
                return redirect('accion_rotacion')

            except Exception as e:
                messages.error(request, f"Error al guardar en la base de datos: {str(e)}")
                return redirect('gestionar_accion', pk=cabecera_obj.idAccion)

    else:
        form_cabecera = AccionPersonalForm(instance=accion_cabecera)

    # OPTIMIZACIÓN COMPATIBLE CON CUALQUIER BD (SQLite/MySQL/PostgreSQL):
    empleados = Empleado.objects.select_related('idPersona').all()
    
    # Mapear el último salario ordenando por ID descendente
    salarios_recientes = {}
    for s in SalarioEmpleado.objects.order_by('idSalarioEmpleado'):
        salarios_recientes[s.idEmpleado_id] = s.Salario_Sem_Neto

    for emp in empleados:
        emp.salario_actual = salarios_recientes.get(emp.pk, 0)

    context = {
        'form_cabecera': form_cabecera,
        'accion_cabecera': accion_cabecera,
        'paso_dos_habilitado': paso_dos_habilitado,
        'empleados': empleados,
        'tipos_accion': DetalleAccion.objects.all(),
        'salarios': SalarioEmpleado.objects.all(),
        'acciones': AccionTipo.objects.select_related(
            'idAccion',
            'id_Detalle_Accion',
            'idAccion__idEmpleado'
        ).order_by('-idAccion_Tipo'),
    }

    return render(request, 'accion_Personal.html', context)


# =========================================================
# OBTENER SALARIO ACTUAL DEL EMPLEADO (AJAX)
# =========================================================
@requiere_permiso("acciones_personal", "ver")
def obtener_salario_empleado(request):
    id_empleado = request.GET.get("idEmpleado")
    salario = SalarioEmpleado.objects.filter(
        idEmpleado=id_empleado
    ).order_by("-idSalarioEmpleado").first()

    if salario:
        return JsonResponse({
            "success": True,
            "idSalarioEmpleado": salario.idSalarioEmpleado,
            "salario": float(salario.Salario_Sem_Neto)
        })

    return JsonResponse({
        "success": False,
        "mensaje": "El empleado no posee salario registrado."
    })


# =========================================================
# OBTENER PREMIO DEL EMPLEADO (AJAX)
# =========================================================
@requiere_permiso("acciones_personal", "ver")
def obtener_premio_empleado(request):
    id_empleado = request.GET.get("idEmpleado")
    premio = PremioAsignado.objects.filter(
        id_KPI__idEmpleado=id_empleado
    ).select_related("idPremio").order_by("-Fecha_Registro").first()

    if premio:
        return JsonResponse({
            "success": True,
            "idPremioAsignado": premio.id_PremioAsignado,
            "monto": float(premio.Monto_Liquidado),
            "descripcion": premio.idPremio.Descripcion
        })

    return JsonResponse({
        "success": False,
        "mensaje": "El empleado no posee premios registrados."
    })


# =========================================================
# ROTACIÓN DE PERSONAL
# =========================================================
@requiere_permiso("acciones_personal", "ver") # ← Normalizado al slug 'acciones_personal'
def rotacion_personal(request):
    data_calculada = {}
    registro = {}

    if request.method == "POST":
        action = request.POST.get("action")
        
        anio = int(request.POST.get("Anio"))
        mes = request.POST.get("Mes")
        mes = int(mes) if mes else None

        # Contrataciones
        contratados = Onboarding.objects.filter(Fecha_Inicio__year=anio)
        if mes:
            contratados = contratados.filter(Fecha_Inicio__month=mes)
        A_Contratados = contratados.count()

        # Desvinculaciones
        desvinculados = Offboarding.objects.filter(Fecha_Salida__year=anio)
        if mes:
            desvinculados = desvinculados.filter(Fecha_Salida__month=mes)

        D_Desvinculados = desvinculados.exclude(
            idCausa__Categoria__in=["Retiro", "Fuerza Mayor"]
        ).count()

        D_Jubilaciones_Defuncionales = desvinculados.filter(
            idCausa__Categoria__in=["Retiro", "Fuerza Mayor"]
        ).count()

        D_Total_Bajas = D_Desvinculados + D_Jubilaciones_Defuncionales

        # Personal Inicial
        if mes:
            empleados_inicio = Empleado.objects.filter(
                Fecha_Ingreso__lt=f"{anio}-{mes:02d}-01",
                Activo=True
            ).count()
        else:
            empleados_inicio = Empleado.objects.filter(
                Fecha_Ingreso__year__lt=anio,
                Activo=True
            ).count()

        F1_Inicio = empleados_inicio
        F2_Final = F1_Inicio + A_Contratados - D_Total_Bajas
        promedio = (F1_Inicio + F2_Final) / 2

        if promedio > 0:
            IRP = round((D_Total_Bajas / promedio) * 100, 2)
        else:
            IRP = Decimal("0.00")

        IRP_Sugerido_Min = Decimal("1.00")
        IRP_Sugerido_Max = Decimal("4.00")

        data_calculada = {
            "A_Contratados": A_Contratados,
            "D_Desvinculados": D_Desvinculados,
            "D_Jubilaciones_Defuncionales": D_Jubilaciones_Defuncionales,
            "D_Total_Bajas": D_Total_Bajas,
            "F1_Inicio": F1_Inicio,
            "F2_Final": F2_Final,
            "irp": IRP,
            "irp_Sugerido_min": IRP_Sugerido_Min,
            "irp_Sugerido_max": IRP_Sugerido_Max,
        }

        registro = {"Anio": anio, "Mes": mes}

        # Guardar Historial
        if action == "guardar":
            try:
                RotacionPersonal.objects.create(
                    Anio=anio,
                    Mes=mes,
                    A_Contratados=A_Contratados,
                    D_Desvinculados=D_Desvinculados,
                    D_Jubilaciones_Defuncionales=D_Jubilaciones_Defuncionales,
                    D_Total_Bajas=D_Total_Bajas,
                    F1_Inicio=F1_Inicio,
                    F2_Final=F2_Final,
                    IRP=IRP,
                    IRP_Sugerido_Min=IRP_Sugerido_Min,
                    IRP_Sugerido_Max=IRP_Sugerido_Max
                )
                messages.success(request, "Historial del período guardado correctamente.")
            except IntegrityError as e:
                messages.error(request, str(e))

    context = {
        "registro": registro,
        "data_calculada": data_calculada,
        "historial": RotacionPersonal.objects.order_by("-Anio", "-Mes")
    }

    return render(request, "rotacion_Personal.html", context)



def evaluaciones_view(request):
    return render(request, 'evaluaciones.html')


# =========================================================
# CREAR EVALUACIÓN + DESEMPEÑO (CABECERA + DETALLE)
# =========================================================
@requiere_permiso("evaluaciones", "ver")
def crear_evaluacion(request):

    empleados = Empleado.objects.select_related(
        "idPersona"
    ).all()

    evaluadores = Empleado.objects.select_related(
        "idPersona"
    ).all()

    periodos = Periodo.objects.all()

    if request.method == "POST":

        bloqueo = bloquear_si_no_puede(
            request,
            "evaluacion_desempeno",
            "crear"
        )

        if bloqueo:
            return bloqueo

        try:

            with transaction.atomic():

                # ============================
                # CABECERA
                # ============================
                idEmpleado = request.POST.get("idEmpleado")
                idEvaluador = request.POST.get("idEvaluador")
                fecha = request.POST.get("Fecha_Evaluacion")
                periodo_id = request.POST.get("periodo")

                evaluacion = Evaluacion.objects.create(

                    Fecha_Evaluacion=fecha,

                    idPeriodo_id=periodo_id,

                    idEmpleado_Ev_id=idEmpleado,

                    idEmpleado_Jef_id=idEvaluador

                )

                # ============================
                # DETALLE
                # ============================
                c1 = request.POST.get("Cumple_Metas_Objetivos") == "1"
                c2 = request.POST.get("Cumple_FuncionesAsig") == "1"
                c3 = request.POST.get("Entregables_Calidad_Tiempo") == "1"
                c4 = request.POST.get("Cumple_Asistencia") == "1"
                c5 = request.POST.get("Muestra_Compromiso_Colaboracion") == "1"

                total = sum([
                    c1,
                    c2,
                    c3,
                    c4,
                    c5
                ])

                pct_total = (total / 5) * 100

                observaciones = request.POST.get(
                    "Observaciones",
                    ""
                )

                EvaluacionDesempeno.objects.create(

                    cumple_metas_objetivos=c1,

                    cumple_funciones_asig=c2,

                    entregables_calidad_tiempo=c3,

                    cumple_asistencia=c4,

                    muestra_compromiso_colaboracion=c5,

                    pct_total_ev=pct_total,

                    observaciones=observaciones,

                    evaluacion=evaluacion

                )

                messages.success(
                    request,
                    "Evaluación registrada correctamente."
                )

                return redirect(
                    "crear_evaluacion"
                )

        except Exception as e:

            messages.error(
                request,
                f"Error al guardar: {str(e)}"
            )

    context = {
        "empleados": empleados,
        "evaluadores": evaluadores,
        "periodos": periodos,
    }

    return render(
        request,
        "eva_Empleado.html",
        context
    )


# =========================================================
# CREAR EVALUACIÓN DE POTENCIAL (JEFATURA)
# =========================================================
@requiere_permiso("evaluaciones", "ver")
def crear_evaluacion_jefatura(request):

    empleados = Empleado.objects.select_related(
        "idPersona"
    ).all()

    evaluadores = Empleado.objects.select_related(
        "idPersona"
    ).all()

    periodos = Periodo.objects.all()

    if request.method == "POST":

        bloqueo = bloquear_si_no_puede(
            request,
            "evaluacion_jefatura",
            "crear"
        )

        if bloqueo:
            return bloqueo

        try:

            with transaction.atomic():

                # ====================================
                # CABECERA
                # ====================================
                idEmpleado = request.POST.get("idEmpleado")
                idEvaluador = request.POST.get("idEvaluador")
                fecha = request.POST.get("Fecha_Evaluacion")
                periodo_id = request.POST.get("periodo")

                evaluacion = Evaluacion.objects.create(

                    Fecha_Evaluacion=fecha,

                    idPeriodo_id=periodo_id,

                    idEmpleado_Ev_id=idEmpleado,

                    idEmpleado_Jef_id=idEvaluador

                )

                # ====================================
                # DETALLE DE JEFATURA
                # ====================================
                liderazgo = request.POST.get(
                    "Capacidad_Liderazgo"
                ) == "1"

                aprendizaje = request.POST.get(
                    "Aprendizaje_Rapido"
                ) == "1"

                adaptacion = request.POST.get(
                    "Adaptacion_Cambio"
                ) == "1"

                iniciativa = request.POST.get(
                    "Iniciativa_Mejora"
                ) == "1"

                madurez = request.POST.get(
                    "Madurez_Emocional"
                ) == "1"

                observaciones = request.POST.get(
                    "Observaciones"
                )

                total = sum([
                    liderazgo,
                    aprendizaje,
                    adaptacion,
                    iniciativa,
                    madurez
                ])

                pct_total = (total / 5) * 100

                EvaluacionJefePotencial.objects.create(

                    Capacidad_Liderazgo=liderazgo,

                    Aprendizaje_Rapido=aprendizaje,

                    Adaptacion_Cambio=adaptacion,

                    Iniciativa_Mejora=iniciativa,

                    Madurez_Emocional=madurez,

                    pct_totalEv=pct_total,

                    Observaciones=observaciones,

                    idEvaluacion=evaluacion
                )

                messages.success(
                    request,
                    "Evaluación de jefatura registrada correctamente."
                )

                return redirect(
                    "crear_evaluacion_jefatura"
                )

        except Exception as e:

            messages.error(
                request,
                f"Error al guardar: {str(e)}"
            )

    context = {
        "empleados": empleados,
        "evaluadores": evaluadores,
        "periodos": periodos,
    }

    return render(
        request,
        "eva_Jefatura.html",
        context
    )


# =========================================================
# CREAR MATRIZ 9 BOX
# =========================================================
@requiere_permiso("evaluaciones", "crear")
def crear_matriz_9box(request):

    empleados = Empleado.objects.select_related("idPersona").all()
    periodos = Periodo.objects.all()
    perfiles = Cuadrante9BoxPerfil.objects.all()
    cuadrantes = Cuadrante9Box.objects.all()
    desempenos = Cuadrante9BoxDesempeno.objects.all()
    potenciales = Cuadrante9BoxPotencial.objects.all()

    if request.method == "POST":

        bloqueo = bloquear_si_no_puede(
            request,
            "evaluaciones",
            "crear"
        )

        if bloqueo:
            return bloqueo

        try:

            with transaction.atomic():

                UnionMatrizEmp.objects.create(

                    Anio=request.POST.get("Anio"),

                    Plan_Accion=request.POST.get("Plan_Accion"),

                    idPeriodo_id=request.POST.get("periodo"),

                    idCuadrante_9box_id=request.POST.get(
                        "idCuadrante_9box"
                    ),

                    idCuadrante_9box_Perfil_id=request.POST.get(
                        "idCuadrante_9box_Perfil"
                    ),

                    idCuadrante_9box_Desempeno_id=request.POST.get(
                        "idCuadrante_9box_Desempeno"
                    ),

                    idCuadrante_9box_Potencial_id=request.POST.get(
                        "idCuadrante_9box_Potencial"
                    ),

                    idEmpleado_id=request.POST.get(
                        "idEmpleado"
                    )
                )

                messages.success(
                    request,
                    "Matriz 9 Box registrada correctamente."
                )

                return redirect("crear_matriz_9box")

        except Exception as e:

            messages.error(
                request,
                f"Error al guardar: {str(e)}"
            )

    context = {
        "empleados": empleados,
        "periodos": periodos,
        "perfiles": perfiles,
        "cuadrantes": cuadrantes,
        "desempenos": desempenos,
        "potenciales": potenciales,
    }

    return render(
        request,
        "matriz.html",
        context
    )


# =========================================================
# DASHBOARD RESULTADOS
# =========================================================
@requiere_permiso("evaluaciones", "ver")
def dashboard_resultados(request):

    empleados = Empleado.objects.select_related(
        "idPersona"
    ).all()

    periodos = Periodo.objects.all()

    empleado_filtro = request.GET.get(
        "empleado_filtro"
    )

    periodo_filtro = request.GET.get(
        "periodo_filtro"
    )

    anio_filtro = request.GET.get(
        "anio_filtro"
    )

    matriz_seleccionada = None
    potencial_seleccionado = None
    desempeno_seleccionado = None

    porcentaje_total = 0
    titulo_porcentaje = "Sin evaluación"

    if empleado_filtro and periodo_filtro and anio_filtro:

        try:

            matriz_seleccionada = UnionMatrizEmp.objects.select_related(

                "idEmpleado__idPersona",

                "idEmpleado__idPuesto",

                "idPeriodo",

                "idCuadrante_9box",

                "idCuadrante_9box_Desempeno",

                "idCuadrante_9box_Potencial",

                "idCuadrante_9box_Perfil"

            ).filter(

                idEmpleado_id=empleado_filtro,

                idPeriodo_id=periodo_filtro,

                Anio=anio_filtro

            ).first()

            if not matriz_seleccionada:

                messages.warning(
                    request,
                    "No se encontraron resultados para los criterios seleccionados."
                )

            else:

                evaluacion = Evaluacion.objects.filter(

                    idEmpleado_Ev_id=empleado_filtro,

                    idPeriodo_id=periodo_filtro

                ).order_by(
                    "-Fecha_Evaluacion"

                ).first()

                if evaluacion:

                    desempeno_seleccionado = (

                        EvaluacionDesempeno.objects.filter(
                            evaluacion=evaluacion
                        ).first()
                    )

                    if desempeno_seleccionado:

                        porcentaje_total = (
                            desempeno_seleccionado.pct_total_ev or 0
                        )

                        titulo_porcentaje = (
                            "Porcentaje de Desempeño"
                        )

                    else:

                        potencial_seleccionado = (

                            EvaluacionJefePotencial.objects.filter(
                                idEvaluacion=evaluacion
                            ).first()
                        )

                        if potencial_seleccionado:

                            porcentaje_total = (
                                potencial_seleccionado.pct_totalEv or 0
                            )

                            titulo_porcentaje = (
                                "Porcentaje Potencial (Jefatura)"
                            )

        except Exception as e:

            messages.error(
                request,
                f"Error al consultar los datos: {str(e)}"
            )

    context = {
        "empleados": empleados,
        "periodos": periodos,
        "matriz_seleccionada": matriz_seleccionada,
        "potencial_seleccionado": potencial_seleccionado,
        "desempeno_seleccionado": desempeno_seleccionado,
        "porcentaje_total": porcentaje_total,
        "titulo_porcentaje": titulo_porcentaje,

        "empleado_filtro_id": (
            int(empleado_filtro)
            if empleado_filtro else None
        ),

        "periodo_filtro_id": (
            int(periodo_filtro)
            if periodo_filtro else None
        ),

        "anio_filtro_val": anio_filtro or "",
    }

    return render(
        request,
        "result_Evaluacion.html",
        context
    )



def elec_KPI_view(request):
    return render(request, 'elec_KPI.html')


# =========================================================================
# 1. VISTA SÓLO PARA LA CABECERA (Carga inicial y Guardado de Cabecera)
# =========================================================================
@requiere_permiso("kpi", "crear")
def registrar_kpi_view(request):

    kpi_cabecera_id = None
    el_empleado_seleccionado = ""
    el_mes_seleccionado = ""
    el_anio_seleccionado = "2026"

    if request.method == 'POST':

        bloqueo = bloquear_si_no_puede(
            request,
            "kpi",
            "crear"
        )

        if bloqueo:
            return bloqueo

        id_empleado = request.POST.get('idEmpleado')
        mes = request.POST.get('Mes')
        anio = request.POST.get('Anio')

        el_empleado_seleccionado = (
            int(id_empleado)
            if id_empleado else ""
        )

        el_mes_seleccionado = (
            int(mes)
            if mes else ""
        )

        el_anio_seleccionado = (
            int(anio)
            if anio else 2026
        )

        try:

            empleado = Empleado.objects.get(
                pk=id_empleado
            )

            cabecera = KpiCabecera(

                idEmpleado=empleado,

                mes=int(mes),

                anio=int(anio)

            )

            cabecera.save()

            kpi_cabecera_id = cabecera.id_KPI

            messages.success(
                request,
                f"¡Cabecera registrada con éxito! ID Asignado: {kpi_cabecera_id}"
            )

        except IntegrityError:

            messages.error(
                request,
                "Error: Ya existe un registro de KPI para este colaborador en el mes y año seleccionados."
            )

        except Empleado.DoesNotExist:

            messages.error(
                request,
                "El colaborador seleccionado no es válido."
            )

        except (ValueError, TypeError):

            messages.error(
                request,
                "Error: Los datos de mes o año enviados no son válidos."
            )

    empleados = Empleado.objects.filter(
        Activo=True
    )

    categorias = KpiCategoria.objects.all()

    context = {
        'empleados': empleados,
        'categorias': categorias,
        'kpi_cabecera_id': kpi_cabecera_id,
        'el_empleado_seleccionado': el_empleado_seleccionado,
        'el_mes_seleccionado': el_mes_seleccionado,
        'el_anio_seleccionado': el_anio_seleccionado,
    }

    return render(
        request,
        'kpi_Registro.html',
        context
    )


# =========================================================================
# 2. VISTA SÓLO PARA AGREGAR EL DETALLE (Procesamiento independiente)
# =========================================================================
@requiere_permiso("kpi", "crear")
def registrar_kpi_detalle_view(request):

    if request.method == 'POST':

        bloqueo = bloquear_si_no_puede(
            request,
            "kpi",
            "crear"
        )

        if bloqueo:
            return bloqueo

        id_kpi_cabecera = request.POST.get(
            'id_KPI'
        )

        id_categoria = request.POST.get(
            'id_KPI_Categoria'
        )

        pct_alcanzado = request.POST.get(
            'pct_Alcanzado'
        )

        monto_base = request.POST.get(
            'Monto_Base'
        )

        try:

            cabecera = get_object_or_404(
                KpiCabecera,
                pk=id_kpi_cabecera
            )

            categoria = get_object_or_404(
                KpiCategoria,
                pk=id_categoria
            )

            monto_total = (
                float(monto_base)
                *
                (
                    float(pct_alcanzado) / 100.0
                )
            )

            detalle = KpiDetalle(

                id_KPI=cabecera,

                id_KPI_Categoria=categoria,

                pct_Alcanzado=float(
                    pct_alcanzado
                ),

                Monto_Base=float(
                    monto_base
                ),

                Monto_Total=round(
                    monto_total,
                    2
                )
            )

            detalle.save()

            messages.success(
                request,
                f"Indicador '{categoria.tipo_categoria}' añadido exitosamente."
            )

        except IntegrityError:
            messages.error(
                request,
                "Error: Esta categoría ya fue evaluada en este mes para el colaborador."
            )

        except Exception as e:

            messages.error(
                request,
                f"Error al guardar el detalle: {str(e)}"
            )

    return redirect(
        'registrar_kpi'
    )



# =========================================================
# CREAR PREMIO
# =========================================================
@requiere_permiso("kpi", "crear")
def crear_premio(request):

    if request.method == 'POST':

        bloqueo = bloquear_si_no_puede(
            request,
            "kpi",
            "crear"
        )

        if bloqueo:
            return bloqueo

        form = PremioForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                '¡Premio guardado exitosamente!'
            )

            return redirect(
                'crear_premio'
            )

    else:

        form = PremioForm()

    premios = Premio.objects.select_related(

        'id_KPI_Categoria',

        'idCuadrante_9box_Perfil'

    ).all().order_by(
        'idPremio'
    )

    return render(
        request,
        'kpi_Premio.html',
        {
            'form': form,
            'premios': premios,
        }
    )


# =========================================================
# EDITAR PREMIO
# =========================================================
@requiere_permiso("kpi", "editar")
def editar_premio(request, id):

    premio = get_object_or_404(
        Premio,
        pk=id
    )

    if request.method == 'POST':

        bloqueo = bloquear_si_no_puede(
            request,
            "kpi",
            "editar"
        )

        if bloqueo:
            return bloqueo

        form = PremioForm(
            request.POST,
            instance=premio
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Premio actualizado correctamente."
            )

            return redirect(
                'crear_premio'
            )

    else:

        form = PremioForm(
            instance=premio
        )

    premios = Premio.objects.select_related(

        'id_KPI_Categoria',

        'idCuadrante_9box_Perfil'

    ).order_by(
        'idPremio'
    )

    return render(
        request,
        'kpi_Premio.html',
        {
            'form': form,
            'premios': premios,
        }
    )


# =========================================================
# VISTA: GUARDAR PREMIO ASIGNADO
# =========================================================
@requiere_permiso("kpi", "crear")
def guardar_premio_asignado(request):

    # =====================================================
    # MÉTODO POST
    # =====================================================

    if request.method == 'POST':

        bloqueo = bloquear_si_no_puede(
            request,
            "kpi",
            "crear"
        )

        if bloqueo:
            return bloqueo

        # =================================================
        # CREAR FORMULARIO CON LOS DATOS RECIBIDOS
        # =================================================

        form = PremioAsignadoForm(
            request.POST
        )

        # =================================================
        # VALIDAR FORMULARIO
        # =================================================

        if form.is_valid():

            try:

                with transaction.atomic():

                    premio = (
                        form.cleaned_data['idPremio']
                    )

                    kpi = (
                        form.cleaned_data['id_KPI']
                    )

                    fecha_registro = (
                        form.cleaned_data['Fecha_Registro']
                    )

                    detalle_kpi = (
                        KpiDetalle.objects.filter(

                            id_KPI=kpi,

                            id_KPI_Categoria=
                                premio.id_KPI_Categoria

                        ).first()
                    )

                    if detalle_kpi is None:

                        messages.error(
                            request,
                            'No se puede asignar este premio. '
                            'El KPI seleccionado no tiene un '
                            'detalle registrado para la categoría '
                            'asociada al premio.'
                        )

                        return render(
                            request,
                            'kpi_AsigPremio.html',
                            {
                                'form': form,
                                'premios_asignados':
                                    PremioAsignado.objects.select_related(
                                        'idPremio',
                                        'id_KPI',
                                        'id_KPI__idEmpleado',
                                        'id_KPI__idEmpleado__idPersona'
                                    ).order_by(
                                        '-Fecha_Registro'
                                    )
                            }
                        )

                    premio_asignado = PremioAsignado(

                        Fecha_Registro=
                            fecha_registro,

                        idPremio=
                            premio,

                        id_KPI=
                            kpi

                    )

                    premio_asignado.save()

                    messages.success(
                        request,
                        (
                            'El premio fue asignado correctamente. '
                            f'Monto liquidado: '
                            f'{premio_asignado.Monto_Liquidado}'
                        )
                    )

                    return redirect(
                        'guardar_premio_asignado'
                    )

            except IntegrityError as e:

                print(
                    'ERROR DE INTEGRIDAD AL GUARDAR '
                    'PREMIO ASIGNADO:',
                    str(e)
                )

                messages.error(
                    request,
                    (
                        'No fue posible guardar el premio asignado. '
                        'Verifique que los datos seleccionados '
                        'sean válidos.'
                    )
                )

            except ValueError as e:

                print(
                    'ERROR DE VALIDACIÓN AL GUARDAR '
                    'PREMIO ASIGNADO:',
                    str(e)
                )

                messages.error(
                    request,
                    str(e)
                )

            except Exception as e:

                print(
                    'ERROR INESPERADO AL GUARDAR '
                    'PREMIO ASIGNADO:',
                    str(e)
                )

                messages.error(
                    request,
                    (
                        'Ocurrió un error inesperado al guardar '
                        'el premio asignado.'
                    )
                )

        else:
            messages.error(
                request,
                (
                    'Por favor, revise los datos ingresados '
                    'en el formulario.'
                )
            )

    else:

        form = PremioAsignadoForm()

    return render(
        request,
        'kpi_AsigPremio.html',
        {
            'form': form,
            'premios_asignados':
                PremioAsignado.objects.select_related(

                    'idPremio',

                    'id_KPI',

                    'id_KPI__idEmpleado',

                    'id_KPI__idEmpleado__idPersona'
                ).order_by(
                    '-Fecha_Registro'
                )
        }
    )


# =========================================================
# VISTA: OBTENER MONTO LIQUIDADO (AJAX)
# =========================================================
def obtener_monto_liquidado(request, idPremio, id_KPI):

    # =====================================================
    # Calcula el monto liquidado en tiempo real:
    #
    # Premio.Monto + KPI_Detalle.Monto_Total
    #
    # Usado por el JavaScript de kpi_AsigPremio.html
    # para mostrar la vista previa antes de guardar.
    # =====================================================
    try:

        premio = get_object_or_404(Premio, idPremio=idPremio)

        kpi = get_object_or_404(KpiCabecera, id_KPI=id_KPI)

        detalle_kpi = KpiDetalle.objects.filter(

            id_KPI=kpi,

            id_KPI_Categoria=premio.id_KPI_Categoria

        ).first()

        if detalle_kpi is None:
            return JsonResponse({
                'success': False,
                'error': (
                    'No existe un detalle de KPI para la categoría '
                    'asociada al premio seleccionado.'
                )
            })

        monto_liquidado = premio.Monto + detalle_kpi.Monto_Total

        return JsonResponse({
            'success': True,
            'monto_liquidado': float(monto_liquidado)
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# =========================================================================
# VISTA: Dashboard / Historial de KPIs
# =========================================================================
@requiere_permiso("kpi", "ver")
def historial_kpi_view(request):

    # ── Filtros desde GET ─────────────────────────────────────────────────
    empleado_filtro_id = request.GET.get('empleado_filtro', '')
    mes_filtro         = request.GET.get('mes_filtro', '')
    anio_filtro        = request.GET.get('anio_filtro', '')

    # ── Catálogos para los selects ────────────────────────────────────────
    empleados  = Empleado.objects.filter(Activo=True).select_related('idPersona')
    categorias = KpiCategoria.objects.all()

    # ── Historial base ────────────────────────────────────────────────────
    detalles = KpiDetalle.objects.select_related(
        'id_KPI',
        'id_KPI__idEmpleado',
        'id_KPI__idEmpleado__idPersona',
        'id_KPI__idEmpleado__idPuesto',
        'id_KPI_Categoria',
    ).all()

    # ── Aplicar filtros ───────────────────────────────────────────────────
    if empleado_filtro_id:
        detalles = detalles.filter(id_KPI__idEmpleado_id=empleado_filtro_id)

    if mes_filtro:
        detalles = detalles.filter(id_KPI__mes=mes_filtro)

    if anio_filtro:
        detalles = detalles.filter(id_KPI__anio=anio_filtro)

    detalles = detalles.order_by('-id_KPI__anio', '-id_KPI__mes')

    # ── Estadísticas resumen ──────────────────────────────────────────────
    total_kpis = detalles.count()
    total_bonos = detalles.aggregate(t=Sum('Monto_Total'))['t'] or 0
    pct_promedio = detalles.aggregate(p=Avg('pct_Alcanzado'))['p'] or 0

    # Premios asignados en el período filtrado
    premios_qs = PremioAsignado.objects.select_related(
        'idPremio',
        'id_KPI',
        'id_KPI__idEmpleado',
        'id_KPI__idEmpleado__idPersona',
        'idPremio__id_KPI_Categoria',
    ).all()

    if empleado_filtro_id:
        premios_qs = premios_qs.filter(id_KPI__idEmpleado_id=empleado_filtro_id)
    if mes_filtro:
        premios_qs = premios_qs.filter(id_KPI__mes=mes_filtro)
    if anio_filtro:
        premios_qs = premios_qs.filter(id_KPI__anio=anio_filtro)

    total_premios = premios_qs.count()

    # ── Top colaboradores (por porcentaje promedio) ───────────────────────
    top_colaboradores = (
        KpiDetalle.objects
        .values(
            'id_KPI__idEmpleado__idPersona__Nombre_Completo',
            'id_KPI__idEmpleado__idPuesto__Nombre',
            'id_KPI__idEmpleado__idPersona__Foto',
        )
        .annotate(pct_prom=Avg('pct_Alcanzado'))
        .order_by('-pct_prom')[:5]
    )

    # ── Resumen financiero ────────────────────────────────────────────────
    resumen_financiero = (
        KpiDetalle.objects
        .values('id_KPI_Categoria__tipo_categoria')
        .annotate(total=Sum('Monto_Total'))
        .order_by('-total')
    )

    context = {
        'empleados': empleados,
        'categorias': categorias,

        'empleado_filtro_id': empleado_filtro_id,
        'mes_filtro': mes_filtro,
        'anio_filtro': anio_filtro,

        'detalles': detalles,
        'premios_qs': premios_qs,

        'total_kpis': total_kpis,
        'total_bonos': total_bonos,
        'pct_promedio': round(pct_promedio, 2),
        'total_premios': total_premios,

        'top_colaboradores': top_colaboradores,
        'resumen_financiero': resumen_financiero,

        'meses': [
            (1,'Enero'), (2,'Febrero'), (3,'Marzo'), (4,'Abril'),
            (5,'Mayo'), (6,'Junio'), (7,'Julio'), (8,'Agosto'),
            (9,'Septiembre'), (10,'Octubre'), (11,'Noviembre'), (12,'Diciembre'),
        ],
    }

    return render(request, 'kpi.html', context)



# =========================================================
# GUARDAR CABECERA DEL ONBOARDING
# Selección de Departamento y Empleado, y guardado en BD
# =========================================================
@requiere_permiso("onboarding", "ver")
def registrar_onboarding(request, pk=None):

    onboarding = None
    paso_dos_habilitado = False

    if pk:
        onboarding = get_object_or_404(
            Onboarding,
            pk=pk
        )

        paso_dos_habilitado = True

    if request.method == "POST":

        accion = "editar" if onboarding else "crear"

        bloqueo = bloquear_si_no_puede(
            request,
            "onboarding",
            accion
        )

        if bloqueo:
            return bloqueo

        form = OnboardingForm(
            request.POST,
            instance=onboarding
        )

        if form.is_valid():

            nuevo = form.save()

            messages.success(
                request,
                f"Proceso de Onboarding #{nuevo.id_Onboarding} creado correctamente."
            )

            return redirect(
                "gestionar_onboarding",
                pk=nuevo.id_Onboarding
            )

        else:

            messages.error(
                request,
                "Revise los datos del formulario."
            )

    else:

        form = OnboardingForm(
            instance=onboarding
        )

    # =====================================================
    # CARGAR ACTIVIDADES REGISTRADAS
    # =====================================================
    actividades = OnboardingActividad.objects.select_related(
        "idActividad",
        "id_Estatus_Vacante",
        "id_Onboarding"
    ).all().order_by(
        "-id_Onboarding__id_Onboarding"
    )

    context = {
        "form": form,
        "form_detalle": OnboardingActividadForm(),
        "onboarding": onboarding,
        "paso_dos_habilitado": paso_dos_habilitado,
        "actividades": actividades,
    }

    return render(
        request,
        "onboarding.html",
        context
    )


# =========================================================
# GUARDAR DETALLE DE ACTIVIDAD DEL ONBOARDING
# =========================================================
@requiere_permiso("onboarding", "editar")  # O la clave de permiso que utilices
def guardar_detalle_onboarding(request, pk):

    # 1. Obtener el registro principal de Onboarding o lanzar 404
    onboarding = get_object_or_404(Onboarding, pk=pk)

    # 2. Solo procesar si la petición es mediante POST
    if request.method == "POST":
        form = OnboardingActividadForm(request.POST)

        if form.is_valid():
            try:
                detalle = form.save(commit=False)
                detalle.id_Onboarding = onboarding
                detalle.save()

                messages.success(request, "Actividad registrada correctamente.")

            except IntegrityError as e:
                messages.error(
                    request, 
                    f"Error de base de datos al registrar la actividad: {e}"
                )
            except Exception as e:
                messages.error(
                    request, 
                    f"Ocurrió un error inesperado al guardar la actividad: {e}"
                )
        else:
            # Notificar errores específicos de validación del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")

    # 3. Redirigir siempre a la gestión del onboarding
    return redirect("gestionar_onboarding", pk=onboarding.pk)


def elec_Offboarding_view(request):
    return render(request, 'elec_Offboarding.html')


# =========================================================
# GUARDAR CABECERA DEL OFFBOARDING
# Proceso de salida de un empleado
# =========================================================
@requiere_permiso("offboarding", "ver")
def registrar_offboarding(request, pk=None):

    offboarding = None
    paso_dos_habilitado = False

    if pk:
        offboarding = get_object_or_404(
            Offboarding,
            pk=pk
        )

        paso_dos_habilitado = True

    if request.method == "POST":

        accion = "editar" if offboarding else "crear"

        bloqueo = bloquear_si_no_puede(
            request,
            "offboarding",
            accion
        )

        if bloqueo:
            return bloqueo

        form = OffboardingForm(
            request.POST,
            instance=offboarding
        )

        if form.is_valid():

            nuevo = form.save()

            messages.success(
                request,
                f"Proceso de Offboarding #{nuevo.id_Offboarding} creado correctamente."
            )

            return redirect(
                "gestionar_offboarding",
                pk=nuevo.id_Offboarding
            )

        else:

            messages.error(
                request,
                "Revise los datos del formulario."
            )

    else:

        form = OffboardingForm(
            instance=offboarding
        )

    context = {
        "form": form,
        "offboarding": offboarding,
        "paso_dos_habilitado": paso_dos_habilitado,
        "offboardings": Offboarding.objects.select_related(
            "idEmpleado__idPersona",
            "idCausa"
        ).order_by("-Fecha_Salida")
    }

    return render(
        request,
        "registrar_off.html",
        context
    )


# =========================================================
# GUARDAR CHECKLIST DE OFFBOARDING
# Crea o actualiza el checklist correspondiente
# al proceso de Offboarding seleccionado
# =========================================================
@requiere_permiso("offboarding", "ver")
def guardar_checklist_offboarding(request):

    if request.method == "POST":

        try:

            # =====================================================
            # DATOS RECIBIDOS DEL FORMULARIO
            # =====================================================
            id_offboarding = request.POST.get(
                "id_Offboarding"
            )

            id_estatus = request.POST.get(
                "id_Estatus_Vacante"
            )

            fecha_comp = request.POST.get(
                "Fecha_Comp"
            )

            observacion = request.POST.get(
                "Observacion"
            )

            actividades = request.POST.getlist(
                "actividades[]"
            )

            # =====================================================
            # VALIDACIONES
            # =====================================================
            if not id_offboarding:

                messages.error(
                    request,
                    "Debe seleccionar un proceso de Offboarding."
                )

            elif not id_estatus:

                messages.error(
                    request,
                    "Debe seleccionar un estado."
                )

            elif not actividades:

                messages.warning(
                    request,
                    "Debe seleccionar al menos una actividad."
                )

            else:

                # =================================================
                # OBTENER EL OFFBOARDING SELECCIONADO
                # =================================================
                offboarding = get_object_or_404(
                    Offboarding,
                    id_Offboarding=id_offboarding
                )

                # =================================================
                # OBTENER EL ESTADO SELECCIONADO
                # =================================================
                estado = get_object_or_404(
                    Estatus,
                    id_Estatus_Vacante=id_estatus
                )

                # =================================================
                # ¿ES CREAR O EDITAR?
                # =================================================
                try:

                    OffboardingChecklist.objects.get(
                        id_Offboarding=offboarding
                    )

                    accion = "editar"

                except OffboardingChecklist.DoesNotExist:
                    accion = "crear"

                bloqueo = bloquear_si_no_puede(
                    request,
                    "offboarding",
                    accion
                )

                if bloqueo:
                    return bloqueo

                # =================================================
                # CALCULAR PORCENTAJE
                # =================================================

                total_catalogo = OffboardingCatalogo.objects.count()

                total_seleccionadas = len(
                    actividades
                )

                if total_catalogo > 0:

                    pct_listo = round(
                        (
                            total_seleccionadas /
                            total_catalogo
                        ) * 100,
                        2
                    )

                else:

                    pct_listo = Decimal(
                        "0.00"
                    )

                # =================================================
                # TRANSACCIÓN
                # =================================================
                with transaction.atomic():

                    try:

                        checklist = OffboardingChecklist.objects.get(
                            id_Offboarding=offboarding
                        )

                        creado = False

                    except OffboardingChecklist.DoesNotExist:

                        checklist = OffboardingChecklist.objects.create(

                            Fecha_Asignacion=date.today(),

                            Fecha_Comp=(
                                fecha_comp
                                if fecha_comp
                                else None
                            ),

                            Observacion=observacion,

                            pct_listo=pct_listo,

                            id_Offboarding=offboarding,

                            id_Estatus_Vacante=estado
                        )

                        creado = True

                    if not creado:

                        checklist.Fecha_Comp = (
                            fecha_comp
                            if fecha_comp
                            else None
                        )

                        checklist.Observacion = observacion
                        checklist.pct_listo = pct_listo
                        checklist.id_Estatus_Vacante = estado

                        checklist.save()

                    OffboardingChecklistDetalle.objects.filter(
                        id_Check=checklist
                    ).delete()

                    registros_creados = 0

                    for id_catalogo in actividades:

                        actividad = get_object_or_404(
                            OffboardingCatalogo,
                            idCatalogo=id_catalogo
                        )

                        OffboardingChecklistDetalle.objects.create(
                            id_Check=checklist,
                            idCatalogo=actividad,
                            Completado=True
                        )

                        registros_creados += 1

                if creado:
                    messages.success(
                        request,
                        f"Checklist #{checklist.id_Check} creado correctamente para el Offboarding #{offboarding.id_Offboarding}."
                    )

                else:
                    messages.success(
                        request,
                        f"Checklist #{checklist.id_Check} actualizado correctamente."
                    )

        except IntegrityError as e:

            print(
                "ERROR DE INTEGRIDAD:",
                e
            )

            messages.error(
                request,
                f"Error de integridad en la base de datos: {e}"
            )

        except Exception as e:

            print(
                "ERROR:",
                e
            )

            messages.error(
                request,
                f"Error al guardar el checklist: {e}"
            )

    # =========================================================
    # DATOS PARA MOSTRAR LA PÁGINA
    # =========================================================

    offboardings = Offboarding.objects.select_related(
        "idEmpleado",
        "idEmpleado__idPersona",
        "idCausa"

    ).order_by(
        "-Fecha_Salida"
    )

    for proceso in offboardings:
        try:

            proceso.checklist_obj = (
                OffboardingChecklist.objects.get(
                    id_Offboarding=proceso.id_Offboarding
                )
            )

        except OffboardingChecklist.DoesNotExist:
            proceso.checklist_obj = None

    context = {
        "offboardings": offboardings,
        "catalogo": OffboardingCatalogo.objects.order_by(
            "Num_Etapa",
            "idCatalogo"
        ),

        "checklists": OffboardingChecklist.objects.select_related(
            "id_Offboarding",
            "id_Estatus_Vacante"
        ).order_by(
            "-Fecha_Asignacion"
        ),

        "estados": Estatus.objects.order_by(
            "id_Estatus_Vacante"
        )
    }

    return render(
        request,
        "checklist_off.html",
        context
    )


from decimal import Decimal
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction, IntegrityError

# =========================================================
# VISTA: MODIFICAR / CARGAR CHECKLIST EXISTENTE
# =========================================================
@requiere_permiso("offboarding", "editar")
def modificar_checklist_offboarding(request, id_check):
    # 1. Obtener el checklist precargando las relaciones (id_Offboarding y id_Estatus_Vacante)
    checklist = get_object_or_404(
        OffboardingChecklist.objects.select_related("id_Offboarding", "id_Estatus_Vacante"),
        pk=id_check
    )
    
    # Asegurar que la fecha venga en formato string YYYY-MM-DD para el input type="date"
    if checklist.Fecha_Comp and isinstance(checklist.Fecha_Comp, (date, datetime)):
        checklist.Fecha_Comp_formatted = checklist.Fecha_Comp.strftime("%Y-%m-%d")
    else:
        checklist.Fecha_Comp_formatted = checklist.Fecha_Comp

    # 2. Cargar catálogo ordenado
    catalogo = list(OffboardingCatalogo.objects.order_by("Num_Etapa", "idCatalogo"))
    total_catalogo = len(catalogo)

    # 3. Intentar obtener los IDs de las actividades marcadas de la tabla de detalle
    checks_seleccionados = list(
        OffboardingChecklistDetalle.objects.filter(
            id_Check=checklist,
            Completado=True
        ).values_list("idCatalogo_id", flat=True)
    )

    # 4. RESPALDO/FALLBACK: Si no existen detalles pero hay un porcentaje guardado (ej. 15%)
    if not checks_seleccionados and checklist.pct_listo and checklist.pct_listo > 0 and total_catalogo > 0:
        porcentaje_decimal = float(checklist.pct_listo) / 100.0
        cantidad_a_marcar = int(round(total_catalogo * porcentaje_decimal))
        checks_seleccionados = [act.idCatalogo for act in catalogo[:cantidad_a_marcar]]

    # Convertir a enteros puros para evitar desacoples de tipo
    checks_seleccionados = [int(x) for x in checks_seleccionados if x is not None]

    # 5. Obtener lista de offboardings para la tabla principal
    offboardings = Offboarding.objects.select_related(
        "idEmpleado", "idEmpleado__idPersona", "idCausa"
    ).order_by("-Fecha_Salida")

    for proceso in offboardings:
        try:
            proceso.checklist_obj = OffboardingChecklist.objects.get(
                id_Offboarding=proceso.id_Offboarding
            )
        except OffboardingChecklist.DoesNotExist:
            proceso.checklist_obj = None

    context = {
        "modo_edicion": True,
        "checklist": checklist,  # Contiene las claves foráneas listas para ser leídas por el template
        "checks_seleccionados": checks_seleccionados,
        "offboardings": offboardings,
        "catalogo": catalogo,
        "checklists": OffboardingChecklist.objects.select_related(
            "id_Offboarding", "id_Estatus_Vacante"
        ).order_by("-Fecha_Asignacion"),
        "estados": Estatus.objects.order_by("id_Estatus_Vacante")
    }

    return render(request, "checklist_off.html", context)


# =========================================================
# VER CHECKLIST DE OFFBOARDING
# =========================================================
@requiere_permiso("offboarding", "ver")  # O la clave de permiso que utilices
def ver_checklist_offboarding(request, id_check):

    # 1. Obtener la checklist objetivo con todas sus relaciones cargadas
    checklist = get_object_or_404(
        OffboardingChecklist.objects.select_related(
            "id_Offboarding",
            "id_Offboarding__idEmpleado",
            "id_Offboarding__idEmpleado__idPersona",
            "id_Estatus_Vacante"
        ),
        pk=id_check
    )

    # 2. Obtener IDs seleccionados en un conjunto (Set) para búsquedas ultrarrápidas O(1)
    checks_seleccionados = set(
        OffboardingChecklistDetalle.objects.filter(
            id_Check=checklist
        ).values_list(
            "idCatalogo_id",
            flat=True
        )
    )

    # 3. Construir contexto previniendo consultas N+1
    context = {
        "modo_ver": True,
        "checklist": checklist,
        "checks_seleccionados": checks_seleccionados,

        "offboardings": Offboarding.objects.select_related(
            "idEmpleado",
            "idEmpleado__idPersona"
        ).order_by("-Fecha_Salida"),

        "catalogo": OffboardingCatalogo.objects.order_by(
            "Num_Etapa",
            "idCatalogo"
        ),

        "estados": Estatus.objects.order_by("id_Estatus_Vacante"),

        "checklists": OffboardingChecklist.objects.select_related(
            "id_Offboarding",
            "id_Offboarding__idEmpleado",
            "id_Offboarding__idEmpleado__idPersona",
            "id_Estatus_Vacante"
        ).order_by("-Fecha_Asignacion"),
    }

    return render(request, "checklist_off.html", context)



# =========================================================
# GUARDAR USUARIO DEL SISTEMA
# =========================================================
@requiere_permiso("usuarios_sistema", "crear")  # O el decorador de seguridad/permisos que utilices
def guardar_usuario_sistema(request):

    if request.method == "POST":
        # Limpieza inicial de inputs
        correo = request.POST.get("Correo", "").strip()
        contrasenia = request.POST.get("Contrasenia", "").strip()
        id_rol = request.POST.get("idRol")
        id_empleado = request.POST.get("idEmpleado_Admin")
        activo_raw = request.POST.get("Activo")

        # ----------------------------------------------------
        # VALIDACIONES BÁSICAS
        # ----------------------------------------------------
        if not correo:
            messages.error(request, "Debe ingresar un correo electrónico.")
        elif not contrasenia:
            messages.error(request, "Debe ingresar una contraseña.")
        elif not id_rol:
            messages.error(request, "Debe seleccionar un rol.")
        elif not id_empleado:
            messages.error(request, "Debe seleccionar un empleado.")
        elif activo_raw is None or activo_raw == "":
            messages.error(request, "Debe seleccionar el estado del usuario.")
        elif UsuarioSistema.objects.filter(Correo=correo).exists():
            messages.error(request, "Ya existe un usuario registrado con ese correo.")
        elif UsuarioSistema.objects.filter(idEmpleado_Admin=id_empleado).exists():
            messages.error(request, "El empleado seleccionado ya tiene un usuario asignado.")
        else:
            try:
                # Búsquedas directas por PK (sin select_related innecesarios para el INSERT)
                rol = get_object_or_404(Roles, pk=id_rol)
                empleado = get_object_or_404(Empleado, pk=id_empleado)

                # Creación del objeto
                UsuarioSistema.objects.create(
                    Correo=correo,
                    Contrasenia=make_password(contrasenia),
                    idRol=rol,
                    Activo=(activo_raw == "1"),
                    idEmpleado_Admin=empleado
                )

                messages.success(request, "Usuario registrado correctamente.")
                return redirect("guardar_usuario_sistema")

            except IntegrityError as e:
                messages.error(
                    request, 
                    "Error de integridad: El correo o el empleado ya se encuentran vinculados a otro usuario."
                )
            except Exception as e:
                messages.error(request, f"Ocurrió un error al guardar el usuario: {e}")

    # ---------------------------------------------------------
    # DATOS PARA EL TEMPLATE (Solo se ejecutan si no hubo un POST exitoso)
    # ---------------------------------------------------------
    context = {
        "empleados": Empleado.objects.select_related(
            "idPersona", 
            "idPuesto"
        ).filter(
            Activo=True
        ).order_by(
            "idPersona__Nombre_Completo"
        ),

        "roles": Roles.objects.order_by("TipoRol"),

        "usuarios": UsuarioSistema.objects.select_related(
            "idRol",
            "idEmpleado_Admin",
            "idEmpleado_Admin__idPersona",
            "idEmpleado_Admin__idPuesto"
        ).order_by("Correo")
    }

    return render(request, "usuarios.html", context)


# =========================================================
# MODIFICAR USUARIO DEL SISTEMA
# =========================================================
@requiere_permiso("usuarios_sistema", "editar")  # O el decorador de seguridad que utilices
def modificar_usuario_sistema(request, id_Admin):

    # Cargar el usuario objetivo o lanzar 404
    usuario = get_object_or_404(
        UsuarioSistema.objects.select_related("idRol", "idEmpleado_Admin"),
        pk=id_Admin
    )

    if request.method == "POST":
        correo = request.POST.get("Correo", "").strip()
        contrasenia = request.POST.get("Contrasenia", "").strip()
        id_rol = request.POST.get("idRol")
        id_empleado = request.POST.get("idEmpleado_Admin")
        activo_raw = request.POST.get("Activo")

        # ----------------------------------------------------
        # VALIDACIONES (Sin redirects para no perder la entrada)
        # ----------------------------------------------------
        if not correo:
            messages.error(request, "Debe ingresar un correo electrónico.")
        elif not id_rol:
            messages.error(request, "Debe seleccionar un rol.")
        elif not id_empleado:
            messages.error(request, "Debe seleccionar un empleado.")
        elif activo_raw is None or activo_raw == "":
            messages.error(request, "Debe seleccionar el estado del usuario.")
        elif UsuarioSistema.objects.filter(Correo=correo).exclude(pk=id_Admin).exists():
            messages.error(request, "Ya existe otro usuario registrado con ese correo.")
        elif UsuarioSistema.objects.filter(idEmpleado_Admin=id_empleado).exclude(pk=id_Admin).exists():
            messages.error(request, "El empleado seleccionado ya tiene otro usuario asignado.")
        else:
            try:
                rol = get_object_or_404(Roles, pk=id_rol)
                empleado = get_object_or_404(Empleado, pk=id_empleado)

                # Actualización de atributos
                usuario.Correo = correo
                usuario.idRol = rol
                usuario.idEmpleado_Admin = empleado
                usuario.Activo = (activo_raw == "1")

                # Actualizar contraseña solo si se ingresó una nueva
                if contrasenia:
                    usuario.Contrasenia = make_password(contrasenia)

                usuario.save()

                messages.success(request, "Usuario modificado correctamente.")
                return redirect("guardar_usuario_sistema")

            except IntegrityError as e:
                messages.error(
                    request, 
                    "Error de integridad: El correo o el empleado ya pertenecen a otro usuario registrado."
                )
            except Exception as e:
                messages.error(request, f"Ocurrió un error al modificar el usuario: {e}")

    # ---------------------------------------------------------
    # CONTEXTO Y DATOS PARA LA PLANTILLA (Solo si es GET o si falló el POST)
    # ---------------------------------------------------------
    context = {
        "usuario_editar": usuario,
        "empleados": Empleado.objects.select_related(
            "idPersona", 
            "idPuesto"
        ).filter(
            Activo=True
        ).order_by("idPersona__Nombre_Completo"),

        "roles": Roles.objects.order_by("TipoRol"),

        "usuarios": UsuarioSistema.objects.select_related(
            "idRol",
            "idEmpleado_Admin",
            "idEmpleado_Admin__idPersona",
            "idEmpleado_Admin__idPuesto"
        ).order_by("Correo")
    }

    return render(request, "usuarios.html", context)


def login_usuario(request):

    # =========================================================
    # SI EL USUARIO ENVÍA EL FORMULARIO
    # =========================================================
    if request.method == "POST":

        # =====================================================
        # OBTENER DATOS DEL FORMULARIO
        # =====================================================
        correo = request.POST.get(
            "Correo",
            ""
        ).strip()

        contrasenia = request.POST.get(
            "Contrasenia",
            ""
        ).strip()


        # =====================================================
        # VALIDAR CAMPOS VACÍOS
        # =====================================================
        if not correo or not contrasenia:

            messages.error(
                request,
                "Debe ingresar el correo electrónico y la contraseña."
            )

            return render(
                request,
                "login.html"
            )


        # =====================================================
        # BUSCAR USUARIO POR CORREO
        # =====================================================
        usuario = (
            UsuarioSistema.objects
            .filter(
                Correo=correo
            )
            .select_related(
                "idRol",
                "idEmpleado_Admin",
                "idEmpleado_Admin__idPersona",
                "idEmpleado_Admin__idPuesto"
            )
            .first()
        )

        # =====================================================
        # VALIDAR CORREO Y CONTRASEÑA
        # =====================================================
        if (
            usuario is None
            or not check_password(
                contrasenia,
                usuario.Contrasenia
            )
        ):

            messages.error(
                request,
                "El correo electrónico o la contraseña son incorrectos."
            )

            return render(
                request,
                "login.html"
            )

        # =====================================================
        # VALIDAR SI EL USUARIO ESTÁ ACTIVO
        # =====================================================
        if not usuario.Activo:
            messages.error(
                request,
                "Su cuenta se encuentra inactiva. Contacte al administrador del sistema."
            )

            return render(
                request,
                "login.html"
            )


        # =====================================================
        # OBTENER EMPLEADO
        # =====================================================
        empleado = usuario.idEmpleado_Admin

        # =====================================================
        # OBTENER PERSONA
        # =====================================================
        persona = empleado.idPersona

        # =====================================================
        # GUARDAR INFORMACIÓN DEL USUARIO
        # =====================================================
        request.session["usuario_id"] = (
            usuario.id_Admin
        )

        request.session["usuario_correo"] = (
            usuario.Correo
        )

        # =====================================================
        # GUARDAR INFORMACIÓN DEL ROL
        # =====================================================
        request.session["usuario_rol_id"] = (
            usuario.idRol.idRol
        )

        request.session["usuario_rol"] = (
            usuario.idRol.TipoRol
        )

        # =====================================================
        # GUARDAR INFORMACIÓN DEL EMPLEADO
        # =====================================================
        request.session["empleado_id"] = (
            empleado.idEmpleado
        )

        request.session["empleado_nombre"] = (
            persona.Nombre_Completo
        )

        # =====================================================
        # GUARDAR PUESTO
        # =====================================================
        if empleado.idPuesto:
            request.session["empleado_puesto"] = (
                empleado.idPuesto.Nombre
            )

        else:
            request.session["empleado_puesto"] = (
                "Sin puesto"
            )


        # =====================================================
        # NO ES NECESARIO GUARDAR LA FOTO EN LA SESIÓN
        #
        # La foto se obtiene directamente desde Persona
        # en la vista inicio_view.
        # =====================================================
        request.session.pop(
            "empleado_foto",
            None
        )

        # =====================================================
        # MENSAJE DE BIENVENIDA
        # =====================================================
        messages.success(
            request,
            f"Bienvenido(a), {persona.Nombre_Completo}."
        )

        # =====================================================
        # REDIRIGIR AL INICIO
        # =====================================================
        return redirect(
            "inicio"
        )

    # =========================================================
    # MOSTRAR LOGIN
    # =========================================================
    return render(
        request,
        "login.html"
    )


def cerrar_sesion(request):
    logout(request)
    return redirect('login_usuario')



import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
# Asegúrate de importar Empleado desde tus modelos
from .models import AccionTipo, RotacionPersonal, Empleado

@requiere_permiso("acciones_personal", "ver")
def modulo_reportes(request):
    acciones = AccionTipo.objects.select_related(
        'idAccion',
        'idAccion__idEmpleado',
        'idAccion__idEmpleado__idPersona',
        'idAccion__idEmpleado__idPuesto',
        'idAccion__idEmpleado__idPuesto__idDepartamento',
        'id_Detalle_Accion',
        'idSalarioEmpleado',
        'id_PremioAsignado',
        'id_PremioAsignado__idPremio'
    ).order_by('-idAccion__Fecha', '-idAccion_Tipo')

    empleados_dict = {}

    for item in acciones:
        emp = item.idAccion.idEmpleado if item.idAccion else None
        if not emp or not emp.idPersona:
            continue

        emp_id = str(emp.pk)

        if emp_id not in empleados_dict:
            persona = emp.idPersona
            puesto = emp.idPuesto
            departamento = puesto.idDepartamento if puesto and hasattr(puesto, 'idDepartamento') else None

            nombre_completo = getattr(persona, 'Nombre_Completo', str(persona))
            cedula_val = getattr(persona, 'Cedula', '---') or '---'
            nombre_puesto = getattr(puesto, 'Nombre', '---') if puesto else '---'
            nombre_depto = getattr(departamento, 'Nombre', getattr(departamento, 'Nombre_Departamento', '---')) if departamento else '---'

            empleados_dict[emp_id] = {
                'id': emp_id,
                'nombre': str(nombre_completo),
                'cedula': str(cedula_val),
                'puesto': str(nombre_puesto),
                'departamento': str(nombre_depto),
                'acciones': []
            }

        # EXTRAEMOS EL DETALLE REGISTRADO EN ACCION TIPO
        detalle_especifico = item.Detalle or (item.id_Detalle_Accion.Detalle if item.id_Detalle_Accion else '')

        empleados_dict[emp_id]['acciones'].append({
            'tipo': item.id_Detalle_Accion.Accion if item.id_Detalle_Accion else 'Otro',
            'detalle': detalle_especifico,
            'fecha': item.idAccion.Fecha.strftime('%d/%m/%Y') if item.idAccion and item.idAccion.Fecha else '',
            'anio': item.idAccion.Fecha.year if item.idAccion and item.idAccion.Fecha else None,
            'mes': item.idAccion.Fecha.month if item.idAccion and item.idAccion.Fecha else None,
        })

    empleados_json = json.dumps(list(empleados_dict.values()), cls=DjangoJSONEncoder)
    rotaciones = RotacionPersonal.objects.order_by('-Anio', '-Mes')

    
    # Consulta para traer a todos los empleados activos junto con su Persona y Puesto
    todos_los_empleados = Empleado.objects.select_related(
        'idPersona', 
        'idPuesto'
    ).filter(
        Activo=True
    ).order_by('idPersona__Nombre_Completo')

    context = {
        'acciones': acciones,
        'empleados_lista': list(empleados_dict.values()),
        'todos_los_empleados': todos_los_empleados,
        'empleados_data_json': empleados_json,
        'rotaciones': rotaciones,
    }

    return render(request, 'reportes.html', context)





    

def configuraciones_view(request):
    return render(request, 'configuraciones.html')
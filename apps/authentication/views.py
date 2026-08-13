from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
from django.db.models import Max
from datetime import date, datetime
from django.contrib import messages
from django.db import transaction
from django.db import IntegrityError
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Avg, Sum 
from django.db.models import Q # Tener esta importación al inicio de tu archivo views.py
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
import json
from django.core.serializers.json import DjangoJSONEncoder



# Importa todo lo que se encuentra en el archivo models.py
# Donde se encuentran los modelos de las tablas de la base de datos
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


# =========================================================
# Vista: Guardar Gerencia
# =========================================================
# Decorador personalizado: Verifica que el usuario tenga el permiso "ver" 
# en el módulo "estructura_organizacional" antes de ejecutar la vista.
@requiere_permiso("estructura_organizacional", "ver")
def gerencias_view(request):

    # Comprueba si la solicitud es de tipo POST (procesamiento/envío de formulario)
    if request.method == 'POST':
        # Captura el ID de la gerencia desde el formulario.
        # Si tiene valor, se interpretará como edición; si está vacío o no existe, como una creación.
        gerencia_id  = request.POST.get('gerencia_id')  # vacío = nuevo registro

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN SI ES CREAR O MODIFICAR
        # ─────────────────────────────────────────────
        # Control granular de permisos: se evalúa si el usuario puede "editar" o "crear"
        if gerencia_id:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "crear")

        # Si el usuario no tiene los permisos necesarios, la función devuelve una respuesta de bloqueo/error
        if bloqueo:
            return bloqueo

        # Obtiene los datos enviados en el cuerpo del formulario POST
        nombre       = request.POST.get('nombre_gerencia')
        empresa_id   = request.POST.get('empresa')
        
        # Recupera la instancia de la Empresa mediante su clave primaria (Primary Key)
        empresa_obj  = Empresa.objects.get(pk=empresa_id)
 
        # Lógica para actualizar un registro existente
        if gerencia_id:
            # Busca la Gerencia existente por su clave primaria
            gerencia = Gerencia.objects.get(pk=gerencia_id)
            # Actualiza sus propiedades con los valores del formulario
            gerencia.Nombre    = nombre
            gerencia.idEmpresa = empresa_obj
            # Guarda los cambios en la base de datos
            gerencia.save()
        
        # Lógica para crear un nuevo registro
        else:
            # Crea y guarda directamente una nueva instancia de Gerencia
            Gerencia.objects.create(
                Nombre    = nombre,
                idEmpresa = empresa_obj,
            )
 
        # Redirige al usuario a la vista nombrada 'gerencias' (patrón Post/Redirect/Get)
        return redirect('gerencias')
 
    # Solicitud GET: Renderiza la plantilla del formulario y la tabla de registros
    return render(request, 'gerencia.html', {
        # Pasa todas las empresas para llenar el desplegable/select
        'empresas'       : Empresa.objects.all(),
        # Optimiza la consulta cargando de forma eficiente la relación con Empresa (JOIN) y ordenando alfabéticamente
        'gerencias'      : Gerencia.objects.select_related('idEmpresa').order_by('Nombre'),
        # Indica que el formulario no está en modo de edición en la carga inicial
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


# =========================================================
# Vista: Guardar Departamento
# =========================================================
# Decorador personalizado: Garantiza que el usuario tenga el permiso "ver" 
# en el módulo "estructura_organizacional" antes de entrar a la función.
@requiere_permiso("estructura_organizacional", "ver")
def departamentos_view(request):

    # Procesa el envío del formulario mediante la petición POST
    if request.method == 'POST':

        # Obtiene el ID del departamento (si existe en la petición).
        # Un valor presente indica actualización de registro; un valor vacío indica creación.
        departamento_id = request.POST.get('departamento_id')

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN SI ES CREAR O MODIFICAR
        # ─────────────────────────────────────────────
        # Verificación dinámica de permisos según el flujo de la petición
        if departamento_id:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "crear")

        # Si el usuario no tiene los permisos suficientes, retorna la respuesta de bloqueo/redirección
        if bloqueo:
            return bloqueo

        # Extrae los valores del formulario enviado
        nombre = request.POST.get('nombre_departamento')

        # Captura el ID de la gerencia padre asociada y recupera su instancia del modelo
        gerencia_id = request.POST.get('gerencia')
        gerencia_obj = Gerencia.objects.get(pk=gerencia_id)

        # Lógica para modificar un departamento existente
        if departamento_id:
            # Busca la instancia del departamento por su clave primaria
            departamento = Departamento.objects.get(
                pk=departamento_id
            )

            # Asigna los nuevos valores recopilados
            departamento.Nombre = nombre
            departamento.idGerencia = gerencia_obj

            # Persiste las modificaciones en la base de datos
            departamento.save()

        # Lógica para crear un nuevo departamento
        else:
            # Crea e inserta directamente la nueva instancia
            Departamento.objects.create(
                Nombre=nombre,
                idGerencia=gerencia_obj
            )

        # Redirige a la vista de departamentos (patrón POST/Redirect/GET)
        return redirect('departamentos')

    # Petición GET: Carga el formulario vacío y la tabla de datos
    return render(
        request,
        'departamento.html',
        {
            # Carga las gerencias ordenadas y optimiza trayendo la relación con 'idEmpresa'
            'gerencias': Gerencia.objects.select_related(
                'idEmpresa'
            ).order_by('Nombre'),

            # Carga los departamentos optimizando la consulta anidada (JOIN con Gerencia y Empresa)
            # para prevenir el problema de rendimiento por consultas N+1 en el HTML
            'departamentos': Departamento.objects.select_related(
                'idGerencia',
                'idGerencia__idEmpresa'
            ).order_by('Nombre'),

            # Indica que el formulario inicia en modo de creación por defecto
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



# =========================================================
# Vista: Guardar Puesto
# =========================================================
# Decorador personalizado: Verifica que el usuario tenga el permiso "ver" 
# en el módulo "estructura_organizacional" antes de permitir el acceso a la vista.
@requiere_permiso("estructura_organizacional", "ver")
def puestos_view(request):

    # Procesa el envío de datos mediante una petición POST (formulario)
    if request.method == 'POST':

        # Obtiene el ID del puesto desde la petición POST.
        # Si contiene un valor, indica una edición; si viene vacío, es una creación.
        puesto_id = request.POST.get('puesto_id')

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN SI ES CREAR O MODIFICAR
        # ─────────────────────────────────────────────
        # Control granular de permisos: evalúa si el usuario tiene permiso de "editar" o "crear"
        if puesto_id:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "crear")

        # Si el usuario no cumple con el permiso correspondiente, retorna la respuesta de bloqueo
        if bloqueo:
            return bloqueo

        # Obtiene los datos del formulario POST para el puesto
        nombre = request.POST.get('nombre_puesto')
        descripcion = request.POST.get('descripcion')

        # Obtiene la clave del departamento seleccionado y recupera su instancia correspondiente
        departamento_id = request.POST.get('departamento')
        departamento_obj = Departamento.objects.get(
            pk=departamento_id
        )

        # Lógica para modificar un puesto existente
        if puesto_id:

            # Busca la instancia del puesto existente por su clave primaria
            puesto = Puesto.objects.get(
                pk=puesto_id
            )

            # Actualiza los atributos del puesto con los datos del formulario
            puesto.Nombre = nombre
            puesto.Descripcion = descripcion
            puesto.idDepartamento = departamento_obj

            # Persiste las modificaciones en la base de datos
            puesto.save()

        # Lógica para registrar un nuevo puesto
        else:

            # Instancia y guarda directamente el nuevo puesto en la base de datos
            Puesto.objects.create(
                Nombre=nombre,
                Descripcion=descripcion,
                idDepartamento=departamento_obj
            )

        # Redirige a la vista nombrada 'puestos' aplicando el patrón POST/Redirect/GET
        return redirect('puestos')

    # ==========================
    # PRUEBA (Bloque de depuración/log)
    # ==========================

    # Consulta todos los departamentos optimizando la relación ForeignKey con 'idGerencia' (JOIN en SQL)
    departamentos = Departamento.objects.select_related(
        'idGerencia'
    ).order_by('Nombre')

    print("DEPARTAMENTOS ENVIADOS AL TEMPLATE:")

    # Imprime en la consola del servidor los ID y nombres de los departamentos recuperados
    for d in departamentos:
        print(d.id_Departamento, d.Nombre)

    # ==========================
    # GET (Renderizado de la vista)
    # ==========================

    return render(
        request,
        'puesto.html',
        {
            # Pasa la lista de departamentos para poblar el menú desplegable/select
            'departamentos': departamentos,

            # Carga los puestos y realiza un JOIN doble (con Departamento y Gerencia)
            # para evitar consultas N+1 al mostrar la información en la plantilla HTML
            'puestos': Puesto.objects.select_related(
                'idDepartamento',
                'idDepartamento__idGerencia'
            ).order_by('Nombre'),

            # Define que por defecto el formulario no está cargando un puesto para edición
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


# =========================================================
# Vista: Guardar / Editar / Listar Compensación por Puesto
# =========================================================
# Decorador personalizado: Garantiza que el usuario cuente con el permiso "ver" 
# dentro del módulo "estructura_organizacional" antes de ejecutar la función.
@requiere_permiso("estructura_organizacional", "ver")
def compensacion_puesto_view(request):

    # Procesa la solicitud cuando el usuario envía el formulario (solicitud POST)
    if request.method == 'POST':

        # Obtiene el ID del esquema de compensación desde la petición POST.
        # Si contiene un valor, se tratará de una edición; si está vacío, de un nuevo registro.
        compensacion_id = request.POST.get('compensacion_id')

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN SI ES CREAR O MODIFICAR
        # ─────────────────────────────────────────────
        # Control granular de permisos: evalúa dinámicamente el nivel de acceso requerido
        if compensacion_id:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "estructura_organizacional", "crear")

        # Si el usuario no tiene los permisos suficientes, interrumpe el flujo y devuelve la vista de bloqueo/redirección
        if bloqueo:
            return bloqueo

        # Extrae todos los rubros económicos y la vigencia desde el formulario enviado
        salario_bruto = request.POST.get('salario_bruto')
        salario_sem_neto = request.POST.get('salario_sem_neto')
        comision_base = request.POST.get('comision_base')
        variable_base = request.POST.get('variable_base')
        viaticos_alimenticios = request.POST.get('viaticos_alimenticios')
        kilometraje_base = request.POST.get('kilometraje_base')
        bono_base = request.POST.get('bono_base')
        vigencia = request.POST.get('vigencia')

        # Obtiene el ID del puesto asociado y recupera la instancia del modelo Puesto
        puesto_id = request.POST.get('puesto')
        puesto_obj = Puesto.objects.get(
            pk=puesto_id
        )

        # Lógica para modificar un registro de compensación existente
        if compensacion_id:

            # Busca el registro de compensación mediante su clave primaria
            compensacion = Compensacion_Puesto.objects.get(
                pk=compensacion_id
            )

            # Reasigna cada uno de los campos con los nuevos valores del formulario
            compensacion.Salario_Bruto = salario_bruto
            compensacion.Salario_Sem_Neto = salario_sem_neto
            compensacion.Comision_Base = comision_base
            compensacion.Variable_Base = variable_base
            compensacion.Viaticos_Alimenticios = viaticos_alimenticios
            compensacion.Kilometraje_Base = kilometraje_base
            compensacion.Bono_Base = bono_base
            compensacion.Vigencia = vigencia
            compensacion.idPuesto = puesto_obj

            # Guarda los cambios aplicados en la base de datos
            compensacion.save()

        # Lógica para crear una nueva compensación
        else:

            # Crea e inserta directamente la nueva instancia de Compensacion_Puesto
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

        # Redirige a la vista nombrada 'compensacion_puesto' (patrón POST/Redirect/GET)
        return redirect('compensacion_puesto')

    # Solicitud GET: Carga y muestra la página principal con el formulario y la tabla de registros
    return render(
        request,
        'confi_Puesto.html',
        {
            # Pasa la lista de puestos ordenados por nombre, optimizando la consulta a la relación 'idDepartamento'
            'puestos': Puesto.objects.select_related(
                'idDepartamento'
            ).order_by('Nombre'),

            # Carga el historial de compensaciones ordenado descendentemente por vigencia (-Vigencia),
            # utilizando select_related anidado para traer Puesto y Departamento en una sola consulta SQL
            'compensaciones': Compensacion_Puesto.objects.select_related(
                'idPuesto',
                'idPuesto__idDepartamento'
            ).order_by('-Vigencia'),

            # Indica que el formulario no está en modo de edición en la carga inicial
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


# =========================================================
# Vista: Registrar Personas
# =========================================================
# Decorador de seguridad: Verifica que el usuario posea el permiso "ver" 
# sobre el módulo "empleados" antes de dar acceso a la vista.
@requiere_permiso("empleados", "ver")
def registrar_persona(request):

    # ── POST: crear o modificar ────────────────────────────
    # Procesa la solicitud enviada desde el formulario HTML
    if request.method == 'POST':
        # Captura la acción explícita enviada desde el formulario ('crear' o 'modificar')
        accion     = request.POST.get('accion')      # 'crear' o 'modificar'
        # ID del registro; si no está presente, implica que es un nuevo registro
        persona_id = request.POST.get('persona_id')  # vacío si es nuevo

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN LA ACCIÓN
        # ─────────────────────────────────────────────
        # Validación granular de permisos: verifica "editar" o "crear" según la acción detectada
        if accion == 'modificar':
            bloqueo = bloquear_si_no_puede(request, "empleados", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "empleados", "crear")

        # Retorna la vista o mensaje de bloqueo si el usuario carece de los permisos requeridos
        if bloqueo:
            return bloqueo

        # Extrae los datos de texto del formulario
        nombre     = request.POST.get('nombre_completo')
        cedula     = request.POST.get('cedula')
        sexo_id    = request.POST.get('sexo')
        nacimiento = request.POST.get('fecha_nacimiento')
        telefono   = request.POST.get('telefono')
        celular    = request.POST.get('celular')
        correo     = request.POST.get('correo')
        direccion  = request.POST.get('direccion')
        
        # Obtiene el archivo de imagen adjunto desde la solicitud MULTIPART (request.FILES)
        foto       = request.FILES.get('foto')

        # Recupera el objeto relacionado PersonaSexo por su clave primaria
        sexo_obj = PersonaSexo.objects.get(pk=sexo_id)

        # Lógica para guardar un nuevo registro de Persona
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
            # Asigna la foto en caso de que se haya subido un archivo
            if foto:
                nueva.Foto = foto
            
            # Persiste el nuevo registro en la base de datos
            nueva.save()

        # Lógica para actualizar una persona existente
        elif accion == 'modificar' and persona_id:
            # Recupera la instancia existente por su clave primaria
            persona = Persona.objects.get(pk=persona_id)
            
            # Sobrescribe los atributos con los nuevos valores
            persona.Nombre_Completo  = nombre
            persona.Cedula           = cedula
            persona.idSexo           = sexo_obj
            persona.Fecha_Nacimiento = nacimiento
            persona.Telefono         = telefono
            persona.Celular          = celular
            persona.Correo           = correo
            persona.Direccion        = direccion
            
            # Solo actualiza la imagen si se adjuntó un archivo nuevo
            if foto:                  # solo reemplaza si se subió una nueva
                persona.Foto = foto
                
            # Guarda los cambios en la base de datos
            persona.save()

        # Patrón PRG (Post/Redirect/Get): redirige para limpiar la petición POST 
        # y evitar el reenvío duplicado del formulario al recargar la página
        return redirect('personas')

    # ── GET: mostrar formulario + tabla con todos los registros ──
    # Renderiza el formulario de captura y la lista completa de personas
    return render(request, 'personas.html', {
        # Colección completa del catálogo de sexos/géneros para el elemento <select>
        'sexos'   : PersonaSexo.objects.all(),
        # Consulta optimizada (select_related) para cargar las personas junto con su género en una sola consulta SQL,
        # ordenadas alfabéticamente por su nombre completo
        'personas': Persona.objects.select_related('idSexo')
                                   .all()
                                   .order_by('Nombre_Completo'),
    })


# =========================================================
# Vista: Editar persona
# =========================================================
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
# Vista: Registrar Empleado
# =========================================================
# Decorador de seguridad: Valida que el usuario tenga el permiso "ver" 
# en el módulo "empleados" antes de ejecutar la vista.
@requiere_permiso("empleados", "ver")
def registrar_empleado(request):

    # ── POST: crear o modificar ────────────────────────────
    # Procesa la solicitud cuando el formulario es enviado con datos
    if request.method == 'POST':

        # Captura la acción explícita enviada desde el formulario ('crear' o 'modificar')
        accion      = request.POST.get('accion')        # 'crear' o 'modificar'
        # Captura el ID del empleado (si existe); vendrá vacío si se trata de un nuevo registro
        empleado_id = request.POST.get('empleado_id')   # vacío si es nuevo

        # =========================================================
        # BLOQUEAR SEGÚN LA ACCIÓN
        # =========================================================
        # Control granular de permisos: exige permiso de "editar" para modificar 
        # y de "crear" para insertar un nuevo empleado
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

        # Si el usuario no cumple con el nivel de permiso requerido, interrumpe el flujo
        if bloqueo:
            return bloqueo

        # =========================================================
        # OBTENER DATOS DEL FORMULARIO
        # =========================================================
        # Extrae los IDs de las relaciones y los datos propios del empleado
        persona_id    = request.POST.get('persona')
        puesto_id     = request.POST.get('puesto')
        contrato_id   = request.POST.get('contrato')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        activo        = request.POST.get('activo')     # '1' o '0'

        # =========================================================
        # OBTENER OBJETOS RELACIONADOS
        # =========================================================
        # Recupera las instancias de los modelos foráneos utilizando sus claves primarias (PK)
        persona_obj = Persona.objects.get(
            pk=persona_id
        )

        puesto_obj = Puesto.objects.get(
            pk=puesto_id
        )

        contrato_obj = Contrato.objects.get(
            pk=contrato_id
        )

        # Convierte el valor en texto ('1' o '0') recibido del formulario a un tipo booleano de Python (True/False)
        activo_bool = activo == '1'

        # =========================================================
        # CREAR EMPLEADO
        # =========================================================
        # Lógica para registrar un nuevo empleado
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
        # Lógica para actualizar los datos de un empleado existente
        elif accion == 'modificar' and empleado_id:

            # Recupera la instancia del empleado a editar por su clave primaria
            empleado = Empleado.objects.get(
                pk=empleado_id
            )

            # Actualiza sus campos con las nuevas instancias y valores
            empleado.idPersona = persona_obj

            empleado.idPuesto = puesto_obj

            empleado.idContrato = contrato_obj

            empleado.Fecha_Ingreso = fecha_ingreso

            empleado.Activo = activo_bool

            # Persiste las modificaciones en la base de datos
            empleado.save()

        # =========================================================
        # PATRÓN PRG (Post/Redirect/Get)
        # Evita reenviar el formulario al recargar la página
        # =========================================================

        return redirect('empleados')

    # =========================================================
    # GET: MOSTRAR FORMULARIO + TABLA
    # =========================================================
    # Renderizado inicial del formulario con las opciones para los elementos <select> y la tabla general
    return render(
        request,
        'empleados.html',
        {

            # Carga la lista de personas ordenada alfabéticamente
            'personas':
                Persona.objects.order_by(
                    'Nombre_Completo'
                ),

            # Carga la lista de puestos optimizando la consulta a Departamento mediante select_related
            'puestos':
                Puesto.objects.select_related(
                    'idDepartamento'
                ).order_by(
                    'Nombre'
                ),

            # Carga todos los tipos/contratos disponibles para el menú desplegable
            'contratos':
                Contrato.objects.all(),

            # Carga los empleados trayendo de forma eficiente en una sola consulta SQL (JOIN) 
            # las relaciones con Persona, Puesto y Contrato, ordenándolos por el nombre de la persona
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
# Vista: Registro Pasantes
# =========================================================
# Decorador de seguridad: Verifica que el usuario cuente con el permiso "ver" 
# dentro del módulo "empleados" antes de permitir la ejecución de la vista.
@requiere_permiso("empleados", "ver")
def registrar_pasante(request):

    # ── POST: crear o modificar ────────────────────────────
    # Procesa la petición cuando el usuario envía los datos del formulario
    if request.method == 'POST':

        # Captura la acción a realizar ('crear' o 'modificar') enviada desde el cliente
        accion     = request.POST.get('accion')       # 'crear' o 'modificar'
        # Captura el ID del pasante (si se va a editar); para un nuevo registro vendrá vacío
        pasante_id = request.POST.get('pasante_id')   # vacío si es nuevo

        # =========================================================
        # BLOQUEAR SEGÚN LA ACCIÓN
        # =========================================================
        # Control granular de permisos: aplica la regla de autorización "editar" o "crear" según el caso
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

        # Si el usuario carece de los permisos requeridos, interrumpe la ejecución y retorna la respuesta de bloqueo
        if bloqueo:
            return bloqueo

        # =========================================================
        # OBTENER DATOS DEL FORMULARIO
        # =========================================================
        # Extrae los IDs de las claves foráneas y los datos académicos/laborales del formulario
        persona_id    = request.POST.get('persona')
        puesto_id     = request.POST.get('puesto')
        supervisor_id = request.POST.get('empleado_sup')
        fecha_inicio  = request.POST.get('fecha_inicio')
        # Asigna None (NULL en base de datos) en caso de que la fecha final no sea enviada
        fecha_fin     = request.POST.get('fecha_fin') or None
        universidad   = request.POST.get('universidad')
        carrera       = request.POST.get('carrera')
        tutor_univ    = request.POST.get('tutor_universitario')
        activo        = request.POST.get('activo')       # '1' o '0'

        # =========================================================
        # OBTENER OBJETOS RELACIONADOS
        # =========================================================
        # Recupera las instancias correspondientes a partir de sus claves primarias
        persona_obj = Persona.objects.get(
            pk=persona_id
        )

        puesto_obj = Puesto.objects.get(
            pk=puesto_id
        )

        supervisor_obj = Empleado.objects.get(
            pk=supervisor_id
        )

        # Convierte la cadena '1' o '0' enviada por el formulario en un booleano de Python (True/False)
        activo_bool = activo == '1'

        # =========================================================
        # CREAR PASANTE
        # =========================================================
        # Lógica para registrar un nuevo pasante
        if accion == 'crear' or not accion:

            Pasante.objects.create(

                idPersona=persona_obj,

                idPuesto=puesto_obj,

                idEmpleado_Sup=supervisor_obj,

                Fecha_Inicio=fecha_inicio,

                Fecha_Fin=fecha_fin,

                # Se mantiene el nombre exacto del campo en el modelo ('Univercidad')
                Univercidad=universidad,

                Carrera=carrera,

                # Se mantiene el nombre exacto del campo en el modelo ('Tutor_Univercitario')
                Tutor_Univercitario=tutor_univ,

                Activo=activo_bool,
            )

        # =========================================================
        # MODIFICAR PASANTE
        # =========================================================
        # Lógica para actualizar la información de un pasante existente
        elif accion == 'modificar' and pasante_id:

            # Recupera el objeto Pasante existente desde la base de datos
            pasante = Pasante.objects.get(
                pk=pasante_id
            )

            # Reasigna todos sus campos con los valores actualizados
            pasante.idPersona = persona_obj

            pasante.idPuesto = puesto_obj

            pasante.idEmpleado_Sup = supervisor_obj

            pasante.Fecha_Inicio = fecha_inicio

            pasante.Fecha_Fin = fecha_fin

            pasante.Univercidad = universidad

            pasante.Carrera = carrera

            pasante.Tutor_Univercitario = tutor_univ

            pasante.Activo = activo_bool

            # Guarda los cambios en la base de datos
            pasante.save()

        # =========================================================
        # PATRÓN PRG (Post/Redirect/Get)
        # Evita reenviar el formulario al recargar la página
        # =========================================================

        return redirect(
            'pasantes'
        )

    # =========================================================
    # GET: MOSTRAR FORMULARIO + TABLA
    # =========================================================
    # Renderizado inicial de la plantilla pasantes.html con los catalogos requeridos
    return render(
        request,
        'pasantes.html',
        {

            # Carga la lista general de personas ordenadas alfabéticamente
            'personas':
                Persona.objects.order_by(
                    'Nombre_Completo'
                ),

            # Carga el catálogo de puestos ordenados por nombre
            'puestos':
                Puesto.objects.order_by(
                    'Nombre'
                ),

            # =====================================================
            # OBTENCIÓN DE SUPERVISORES
            # Trae los empleados y realiza un JOIN con Persona para mostrar su nombre
            # =====================================================

            'supervisores':
                Empleado.objects.select_related(
                    'idPersona'
                ).order_by(
                    'idPersona__Nombre_Completo'
                ),

            # =====================================================
            # LISTADO DE PASANTES
            # Optimizado con select_related para evitar N+1 (incluye la relación anidada del supervisor)
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


from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
# Importa tus modelos y decoradores/funciones de permisos según corresponda

# =========================================================
# Vista: Salarios — registro, modificación y listado
# =========================================================
@requiere_permiso("salarios", "ver")  # Exige permiso de lectura en el módulo 'salarios' para acceder a la vista
def registrar_salario(request):

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIONES POST (CREAR / EDITAR)
    # -----------------------------------------------------
    if request.method == 'POST':

        # Captura la acción a realizar ('crear' o 'modificar') y el ID del salario en caso de edición
        accion = request.POST.get('accion')
        salario_id = request.POST.get('salario_id')

        # =====================================================
        # BLOQUEAR SEGÚN LA ACCIÓN (VERIFICACIÓN DE PERMISOS)
        # =====================================================
        # Evalúa dinámicamente si el usuario posee permiso específico para 'editar' o 'crear'
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

        # Si el usuario no tiene permisos, se interrumpe el flujo y se retorna la respuesta de bloqueo (ej. 403 u otra vista)
        if bloqueo:
            return bloqueo

        # =====================================================
        # DATOS DEL FORMULARIO
        # =====================================================
        # Extracción y casteo de datos del POST. Se asigna 0 por defecto a los numéricos si vienen vacíos.
        empleado_id = request.POST.get('empleado')

        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

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

        observaciones = request.POST.get('observaciones')

        # =====================================================
        # OBTENER EMPLEADO
        # =====================================================
        # Busca la instancia del empleado asociado. (Nota: get_object_or_404 es más seguro si el ID puede ser inválido)
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
                ),  # Si la fecha_fin está vacía, guarda un valor NULL en BD
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

            # Obtiene el salario a editar o lanza un HTTP 404 si el ID no existe
            salario = get_object_or_404(
                SalarioEmpleado,
                pk=salario_id
            )

            # Actualiza cada campo con los nuevos valores del formulario
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

            # Guarda los cambios en la base de datos
            salario.save()

        # =====================================================
        # PATRÓN PRG (Post/Redirect/Get)
        # =====================================================
        # Redirige para evitar el reenvío duplicado de formularios al recargar la página
        return redirect('salarios')

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIONES GET (MOSTRAR VISTA)
    # -----------------------------------------------------
    # Carga datos adicionales si se pasa un ID por parámetro GET (ej: ?editar=123)
    salario_id_editar = request.GET.get('editar')
    salario_editar = None
    if salario_id_editar:
        salario_editar = get_object_or_404(SalarioEmpleado, pk=salario_id_editar)

    return render(
        request,
        'salario.html',
        {
            # Carga empleados activos optimizando la consulta SQL con select_related
            'empleados': Empleado.objects.select_related(
                'idPersona',
                'idPuesto'
            ).filter(
                Activo=True
            ).order_by(
                'idPersona__Nombre_Completo'
            ),

            # Carga el historial de salarios optimizando lecturas de relaciones y ordenando del más reciente al más antiguo
            'salarios': SalarioEmpleado.objects.select_related(
                'idEmpleado',
                'idEmpleado__idPersona',
                'idEmpleado__idPuesto'
            ).order_by(
                '-Fecha_Inicio'
            ),

            # Pasa el objeto a editar si existe, o None si es un registro nuevo
            'salario_editar': salario_editar
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
# Obtener compensación base según el puesto del empleado (API Endpoint)
# =========================================================
@requiere_permiso("salarios", "ver")  # Exige permiso de lectura en 'salarios' para consultar estos datos
def obtener_compensacion_empleado(
    request,
    id_empleado
):

    try:
        # -----------------------------------------------------
        # 1. BÚSQUEDA DEL EMPLEADO Y SU PUESTO
        # -----------------------------------------------------
        # Carga el empleado optimizando la consulta a la tabla 'Puesto' mediante select_related
        empleado = Empleado.objects.select_related(
            'idPuesto'
        ).get(
            pk=id_empleado
        )

        # Logs en consola para depuración durante el desarrollo
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

        # -----------------------------------------------------
        # 2. BÚSQUEDA DE COMPENSACIONES VIGENTES
        # -----------------------------------------------------
        # Filtra las compensaciones configuradas para el puesto del empleado
        compensaciones = Compensacion_Puesto.objects.filter(
            idPuesto=empleado.idPuesto
        )

        print(
            "COMPENSACIONES ENCONTRADAS:",
            compensaciones.count()
        )

        # Obtiene la compensación más reciente aplicando un orden descendente por 'Vigencia'
        compensacion = compensaciones.order_by(
            '-Vigencia'
        ).first()

        # =====================================================
        # CASO 1: NO EXISTE COMPENSACIÓN CONFIGURADA
        # =====================================================
        if compensacion is None:

            return JsonResponse({

                'success': False,

                'mensaje':
                    'El puesto no tiene compensación configurada.'
            })

        # =====================================================
        # CASO 2: RETORNAR COMPENSACIÓN EXITOSA
        # =====================================================
        # Se convierten los valores Decimal de la BD a float para ser serializables a JSON
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

            # Formatea la fecha de vigencia a YYYY-MM-DD o None si está vacía
            'vigencia':
                compensacion.Vigencia.strftime(
                    '%Y-%m-%d'
                )
                if compensacion.Vigencia
                else None

        })

    # =====================================================
    # CONTROL DE EXCEPCIONES: EMPLEADO NO ENCONTRADO
    # =====================================================
    except Empleado.DoesNotExist:

        return JsonResponse({

            'success': False,

            'mensaje':
                'Empleado no encontrado.'
        })

    # =====================================================
    # CONTROL DE EXCEPCIONES: ERROR GENERAL NO CONTROLADO
    # =====================================================
    except Exception as e:

        return JsonResponse({

            'success': False,

            'mensaje':
                str(e)
        })



def reclutamiento_view(request):
    return render(request, 'reclutamiento.html')


# =========================================================
# Vista: Vacantes — Registro, Modificación y Listado
# =========================================================
@requiere_permiso("reclutamiento", "ver")  # Control de acceso general: Requiere permiso 'ver' en el módulo 'reclutamiento'
def registrar_vacante(request):

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIONES POST (CREAR / EDITAR)
    # -----------------------------------------------------
    if request.method == 'POST':

        # Obtención de variables de control del formulario
        accion = request.POST.get('accion')
        vacante_asig_id = request.POST.get('vacante_asig_id')

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN LA ACCIÓN (CONTROL DE PERMISOS)
        # ─────────────────────────────────────────────
        # Se verifica dinámicamente si el usuario tiene permiso para crear o editar
        if accion == 'modificar':
            bloqueo = bloquear_si_no_puede(request, "reclutamiento", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "reclutamiento", "crear")

        # Si el usuario no cuenta con el permiso requerido, se interrumpe y retorna la respuesta de bloqueo
        if bloqueo:
            return bloqueo

        # =====================================================
        # EXTRAER DATOS PROPIOS DE LA VACANTE
        # =====================================================
        fecha_registro = request.POST.get('fecha_registro')
        titulo = request.POST.get('titulo_publicacion')
        motivo = request.POST.get('motivo')
        experiencia = request.POST.get('experiencia_requerida')
        salario_bruto = request.POST.get('salario_bruto')
        compensacion_total = request.POST.get('compensacion_total')
        cierre = request.POST.get('cierre_proceso')

        # =====================================================
        # EXTRAER LLAVES FORÁNEAS Y RELACIONES
        # =====================================================
        estatus_id = request.POST.get('estatus')

        empleado_aut_id = request.POST.get('empleado_aut')      # Empleado que autoriza
        empleado_eval_id = request.POST.get('empleado_eval')    # Empleado que evalúa
        empleado_jefe_id = request.POST.get('empleado_jefe')    # Jefe del puesto
        empleado_sus_id = request.POST.get('empleado_sus')      # Empleado a sustituir (opcional)
        puesto_id = request.POST.get('puesto')

        # Logs de depuración en consola
        print("SALARIO BRUTO:", salario_bruto)
        print("COMPENSACION TOTAL:", compensacion_total)
        
        # =====================================================
        # CREAR NUEVA VACANTE Y ASIGNACIÓN
        # =====================================================
        if accion == 'crear':

            # 1. Crear el registro principal de la Vacante
            vacante = Vacante.objects.create(
                Fecha_Registro=fecha_registro,
                TituloPublicacion=titulo,
                Motivo=motivo,
                Expe_Requerida=experiencia,
                Salario_Bruto=salario_bruto,
                Compensacion_Total=compensacion_total,
                Cierre_Proceso=cierre if cierre else None  # Evita guardar cadenas vacías en campos de tipo Date/Null
            )

            # 2. Crear la asignación intermedia vinculando la vacante con estatus, puesto y responsables
            # Nota: Usar el sufijo '_id' permite asignar directamente la PK sin hacer una consulta extra a la BD
            Vacante_Asig.objects.create(
                id_Vacante=vacante,
                id_Estatus_Vacante_id=estatus_id,
                idEmpleado_Aut_id=empleado_aut_id,
                idEmpleado_Rel_Ev_id=empleado_eval_id,
                idEmpleado_Jef_Puest_id=empleado_jefe_id,
                idEmpleado_Sus_id=(
                    empleado_sus_id
                    if empleado_sus_id else None  # Asigna NULL si no hay empleado a sustituir
                ),
                idPuesto_id=puesto_id
            )

        # =====================================================
        # MODIFICAR VACANTE Y ASIGNACIÓN EXISTENTE
        # =====================================================
        elif accion == 'modificar':

            # Obtiene el registro de asignación existente o retorna un error HTTP 404 si el ID no es válido
            asignacion = get_object_or_404(
                Vacante_Asig,
                pk=vacante_asig_id
            )

            # Obtiene la instancia del modelo Vacante vinculada
            vacante = asignacion.id_Vacante

            # Actualizar campos del modelo principal Vacante
            vacante.Fecha_Registro = fecha_registro
            vacante.TituloPublicacion = titulo
            vacante.Motivo = motivo
            vacante.Expe_Requerida = experiencia
            vacante.Salario_Bruto = salario_bruto
            vacante.Compensacion_Total = compensacion_total
            vacante.Cierre_Proceso = (
                cierre if cierre else None
            )
            vacante.save()  # Guarda los cambios de la vacante en la BD

            # Actualizar llaves foráneas en el modelo de Asignación
            asignacion.id_Estatus_Vacante_id = estatus_id
            asignacion.idEmpleado_Aut_id = empleado_aut_id
            asignacion.idEmpleado_Rel_Ev_id = empleado_eval_id
            asignacion.idEmpleado_Jef_Puest_id = empleado_jefe_id
            asignacion.idEmpleado_Sus_id = (
                empleado_sus_id if empleado_sus_id else None
            )
            asignacion.idPuesto_id = puesto_id
            asignacion.save()  # Guarda los cambios de la asignación en la BD

        # Aplicación del patrón PRG (Post/Redirect/Get) para evitar reenvíos de formulario al recargar
        return redirect('vacantes')
    
    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIONES GET (MOSTRAR PANTALLA)
    # -----------------------------------------------------
    return render(
        request,
        'vacante.html',
        {
            'vacante_editar': None,

            # Catálogos para poblar los controles del formulario
            'estatuses': Estatus.objects.all(),

            'empleados': Empleado.objects.select_related(
                'idPersona'
            ),

            'puestos': Puesto.objects.all(),

            # Consulta optimizada con select_related para traer todas las relaciones
            # de la vacante y las personas asociadas en un solo JOIN de SQL (evita el problema de consultas N+1)
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


# =========================================================
# Vista: Cargar pantalla para Editar un Candidato
# =========================================================
@requiere_permiso("reclutamiento", "editar")  # Restringe la acción específicamente a usuarios con permiso de edición
def editar_candidato(request, id):
    """
    Recupera la información de un registro de candidato específico
    y renderiza la plantilla principal de reclutamiento prellenando
    el formulario con sus datos actuales.
    """

    # 1. Búsqueda del candidato por ID en la BD (o devuelve 404 si no existe)
    candidato = get_object_or_404(
        Vacante_Candidato,
        pk=id
    )

    # 2. Construcción del contexto para el renderizado del template
    contexto = {
        # Pasa el objeto específico para que la plantilla identifique el modo edición
        # y pre-llene los campos del formulario con los valores actuales
        'candidato_editar': candidato,

        # Catálogos para poblar las opciones desplegables (<select>) del formulario
        'personas': Persona.objects.all(),
        'vacantes': Vacante.objects.all(),
        'fases': FaseCandidato.objects.all(),
        'procesos': ProcesoFase.objects.all(),

        # Consulta optimizada con select_related para mantener visible la tabla
        # con todos los candidatos registrados sin generar consultas N+1 a la BD
        'candidatos': Vacante_Candidato.objects.select_related(
            'idPersona',
            'id_Vacante',
            'id_Fase',
            'id_Proceso'
        )
    }

    # Reutiliza el mismo template principal ('reclut_Vacante.html') 
    # enviándole el contexto configurado en modo edición
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
@requiere_permiso("vacaciones", "ver")  # Exige permiso de lectura en el módulo 'vacaciones' para ingresar
def registrar_solicitud_vacacion(request):

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIONES POST (CREAR / EDITAR)
    # -----------------------------------------------------
    if request.method == 'POST':

        # Captura la acción a realizar ('crear' o 'modificar') y el ID en caso de edición
        accion = request.POST.get('accion')
        solicitud_id = request.POST.get('solicitud_id')

        # ─────────────────────────────────────────────
        # BLOQUEAR SEGÚN LA ACCIÓN (CONTROL DE PERMISOS)
        # ─────────────────────────────────────────────
        # Evalúa si el usuario tiene permiso explícito para 'editar' o 'crear' en vacaciones
        if accion == 'modificar':
            bloqueo = bloquear_si_no_puede(request, "vacaciones", "editar")
        else:
            bloqueo = bloquear_si_no_puede(request, "vacaciones", "crear")

        # Si no posee el permiso, se interrumpe la ejecución enviando la vista/respuesta de bloqueo
        if bloqueo:
            return bloqueo

        # ============================================
        # CREAR NUEVA SOLICITUD DE VACACIONES
        # ============================================
        if accion == 'crear':

            # Registra la nueva solicitud mapeando los nombres del formulario POST.
            # Nota: El uso de '_id' asigna directamente las Foreign Keys sin hacer queries extra.
            VacacionSolicitud.objects.create(
                Fecha_Solicitud=request.POST.get('fecha_solicitud'),
                Fecha_Inicio=request.POST.get('fecha_inicio'),
                Fecha_Fin=request.POST.get('fecha_fin'),
                Dias_Solicitud=request.POST.get('dias_solicitados'),
                id_Estatus_Vacante_id=request.POST.get('estado'),
                idEmpleado_Sol_Vac_id=request.POST.get('empleado'),   # Empleado solicitante
                idEmpleado_Respon_id=request.POST.get('aprobador')   # Empleado responsable/aprobador
            )

        # ============================================
        # MODIFICAR SOLICITUD EXISTENTE
        # ============================================
        elif accion == 'modificar':

            # Obtiene la solicitud a editar o lanza un HTTP 404 si el ID es inexistente
            solicitud = get_object_or_404(
                VacacionSolicitud,
                pk=solicitud_id
            )

            # Actualización de atributos con los datos capturados del formulario
            solicitud.Fecha_Solicitud = request.POST.get('fecha_solicitud')
            solicitud.Fecha_Inicio = request.POST.get('fecha_inicio')
            solicitud.Fecha_Fin = request.POST.get('fecha_fin')
            solicitud.Dias_Solicitud = request.POST.get('dias_solicitados')
            solicitud.id_Estatus_Vacante_id = request.POST.get('estado')
            solicitud.idEmpleado_Sol_Vac_id = request.POST.get('empleado')
            solicitud.idEmpleado_Respon_id = request.POST.get('aprobador')

            # Impacta las modificaciones realizadas en la base de datos
            solicitud.save()

        # Patrón PRG (Post/Redirect/Get) para evitar reenvío accidental de datos al refrescar la página
        return redirect('solicitudes_vacaciones')

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIONES GET (MOSTRAR VISTA)
    # -----------------------------------------------------
    contexto = {
        'solicitud_editar': None,

        # Catalogos de opciones para popular los selectores del formulario
        'empleados': Empleado.objects.all(),
        'aprobadores': Empleado.objects.all(),
        'estados': Estatus.objects.all(),

        # Carga optimizada con select_related para traer los datos del solicitante,
        # aprobador y estatus en una sola consulta JOIN de SQL (evita el problema N+1)
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


# =========================================================
# GUARDAR SALDO DE VACACIONES (CON LÓGICA PROGRESIVA ACUMULADA)
# =========================================================
@requiere_permiso("vacaciones", "ver")  # Restringe la vista a usuarios con permisos de lectura
def guardar_saldo_vacaciones(request):

    if request.method == "POST":
        # -----------------------------------------------------
        # 1. VALIDACIÓN DE PERMISOS DE ESCRITURA
        # -----------------------------------------------------
        bloqueo = bloquear_si_no_puede(request, "vacaciones", "crear")
        if bloqueo:
            return bloqueo

        # Obtiene los parámetros enviados desde el formulario POST
        empleado_id = request.POST.get("empleado")
        anio_param = request.POST.get("anio")

        if empleado_id:
            # Obtiene el empleado o lanza error HTTP 404 si no existe
            empleado = get_object_or_404(Empleado, idEmpleado=empleado_id)

            # Casteo seguro del año; si no viene o falla la conversión, asigna el año actual
            try:
                anio = int(anio_param) if anio_param else date.today().year
            except ValueError:
                anio = date.today().year

            # Determina la fecha límite/corte para el cálculo
            hoy = date.today()
            # Si se procesa un año pasado, el corte es al 31 de diciembre; si es el año actual, el corte es hoy
            fecha_corte = date(anio, 12, 31) if anio < hoy.year else hoy

            # -----------------------------------------------------
            # 2. BUSCAR SALDO ANTERIOR DE ESTE EMPLEADO
            # -----------------------------------------------------
            # Busca el último registro de saldo guardado para el empleado de un año previo
            saldo_anterior = VacacionSaldo.objects.filter(
                idEmpleado_Sal_Vac=empleado,
                Anio__lt=anio
            ).order_by('-Anio').first()

            # -----------------------------------------------------
            # 3. CÁLCULO DE DÍAS ACUMULADOS PROGRESIVO
            # -----------------------------------------------------
            if saldo_anterior:
                # Caso A: Existe un saldo histórico previo.
                disponibles_base = float(saldo_anterior.Dias_Disponibles or 0.0)
                inicio_periodo = date(anio, 1, 1)

                if fecha_corte > inicio_periodo:
                    # Calcula días transcurridos dentro del año evaluado
                    dias_en_periodo = (fecha_corte - inicio_periodo).days
                    # Proporcional de días ganados basados en 15 días anuales por norma legal/empresa
                    ganados_periodo = round((dias_en_periodo / 365.0) * 15, 2)
                else:
                    ganados_periodo = 0.0

                # Suma los días remanentes del periodo anterior con los nuevos ganados
                acumulados = round(disponibles_base + ganados_periodo, 2)
            else:
                # Caso B: Primer año del empleado (sin saldo histórico).
                # Compatibilidad para buscar el campo de fecha de ingreso en minúscula o Mayúscula
                fecha_ingreso = getattr(empleado, 'Fecha_Ingreso', None) or getattr(empleado, 'fecha_ingreso', None)
                
                if fecha_ingreso and fecha_corte > fecha_ingreso:
                    # Calcula proporcional desde la fecha real de ingreso a la empresa
                    dias_trabajados = (fecha_corte - fecha_ingreso).days
                    acumulados = round((dias_trabajados / 365.0) * 15, 2)
                else:
                    acumulados = 0.0

            # -----------------------------------------------------
            # 4. SOLICITUDES DE VACACIONES TOMADAS EN EL AÑO CONSULTADO
            # -----------------------------------------------------
            # Consulta solicitudes aprobadas en el año indicado
            solicitudes = VacacionSolicitud.objects.filter(
                idEmpleado_Sol_Vac=empleado,
                id_Estatus_Vacante__TipoEstatus__icontains="aprobad",
                Fecha_Inicio__year=anio
            )
            # Agregación SQL para sumar el total de días tomados
            suma_tomados = solicitudes.aggregate(total=Sum('Dias_Solicitud'))['total']
            tomados = float(suma_tomados) if suma_tomados is not None else 0.0

            # -----------------------------------------------------
            # 5. DÍAS DISPONIBLES FINALES
            # -----------------------------------------------------
            # Diferencia entre acumulados ganados y tomados efectivamente
            disponibles = round(acumulados - tomados, 2)

            # -----------------------------------------------------
            # 6. GUARDAR / ACTUALIZAR EN BASE DE DATOS
            # -----------------------------------------------------
            # Obtiene o crea la tupla de registro para evitar duplicidad del par (Empleado, Año)
            saldo, creado = VacacionSaldo.objects.get_or_create(
                idEmpleado_Sal_Vac=empleado,
                Anio=anio
            )

            # Actualiza los campos calculados directamente vía queryset para optimizar escritura
            VacacionSaldo.objects.filter(pk=saldo.pk).update(
                Dias_Acumulados=acumulados,
                Dias_Tomado=tomados,
                Dias_Disponibles=disponibles
            )

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIÓN GET O RE-RENDERIZADO POST
    # -----------------------------------------------------
    # Carga optimizada de tablas relacionadas usando select_related
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
@requiere_permiso("asistencia", "ver")  # Exige permiso de lectura en el módulo 'asistencia' para acceder
def guardar_asistencia(request):

    # Carga de catálogos base para los desplegables de la plantilla
    # Optimizado con select_related para traer la información personal del empleado
    empleados = Empleado.objects.select_related(
        'idPersona'
    )
    estados = AsistenciaEstado.objects.all()

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIONES POST (CREAR ASISTENCIA)
    # -----------------------------------------------------
    if request.method == "POST":

        # ==========================================
        # VALIDAR PERMISO PARA CREAR
        # ==========================================
        # Restringe la acción si el usuario no cuenta con privilegios de creación
        bloqueo = bloquear_si_no_puede(
            request,
            "asistencia",
            "crear"
        )

        if bloqueo:
            return bloqueo

        # Obtención de las instancias de modelos relacionadas a partir de los IDs enviados por POST
        empleado = Empleado.objects.get(
            idEmpleado=request.POST.get("empleado")
        )

        estado = AsistenciaEstado.objects.get(
            idAsis_Estado=request.POST.get("estado")
        )

        # Convierte las cadenas de texto del formulario ("HH:MM") a objetos de tipo datetime.time
        hora_entrada = datetime.strptime(
            request.POST.get("hora_entrada"),
            "%H:%M"
        ).time()

        hora_salida = datetime.strptime(
            request.POST.get("hora_salida"),
            "%H:%M"
        ).time()

        # Construcción de la nueva instancia del modelo Asistencia
        asistencia = Asistencia(
            Fecha=request.POST.get("fecha"),
            Hora_Entrada=hora_entrada,
            Hora_Salida=hora_salida,
            idEmpleado=empleado,
            idAsis_Estado=estado
        )

        # Guarda la asistencia en BD (dispara la lógica interna del método save() del modelo, 
        # como el cálculo automático de Horas_Extra si está implementado allí)
        asistencia.save()

    # -----------------------------------------------------
    # RENDERIZADO DE PANTALLA Y TABLA DE ASISTENCIAS
    # -----------------------------------------------------
    # Consulta optimizada con select_related multinivel para traer en una sola consulta
    # la asistencia, los datos del empleado, su persona asociada y el estado de asistencia
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
@requiere_permiso("permisos", "crear")  # Exige permiso específico de creación en el módulo 'permisos'
def guardar_permiso(request):

    # ==========================================
    # 1. CARGA DE CATÁLOGOS BASE Y FILTROS
    # ==========================================
    
    # Consulta optimizada para traer empleados junto con los datos de su Persona relacionada (JOIN)
    empleados = Empleado.objects.select_related(
        'idPersona'
    )

    # Catálogo con la lista completa de tipos de permiso disponibles
    tipos_permiso = TipoPermiso.objects.all()

    # Filtra únicamente las asistencias cuyo estado corresponda a "Permiso", 
    # evitando vincular permisos a asistencias normales o faltas. 
    # Incluye select_related multinivel para evitar consultas N+1 en la UI.
    asistencias_permiso = Asistencia.objects.select_related(
        'idEmpleado',
        'idEmpleado__idPersona',
        'idAsis_Estado'
    ).filter(
        idAsis_Estado__TipoEstado='Permiso'
    )

    # ==========================================
    # 2. PROCESAMIENTO DE PETICIÓN POST (GUARDAR)
    # ==========================================
    if request.method == "POST":

        # ─────────────────────────────────────────────
        # VALIDAR PERMISO PARA CREAR EN TIEMPO DE EJECUCIÓN
        # ─────────────────────────────────────────────
        bloqueo = bloquear_si_no_puede(
            request,
            "permisos",
            "crear"
        )

        # Si la validación falla, interrumpe el flujo y retorna la respuesta de restricción
        if bloqueo:
            return bloqueo

        # Obtención de las instancias de los modelos relacionados mediante los IDs del formulario
        empleado = Empleado.objects.get(
            idEmpleado=request.POST.get("empleado")
        )

        asistencia = Asistencia.objects.get(
            idAsistencia=request.POST.get("asistencia")
        )

        tipo_permiso = TipoPermiso.objects.get(
            id_TipoPermiso=request.POST.get("tipo_permiso")
        )

        # Captura y evaluación del flag de estado activo/inactivo
        activo = request.POST.get("activo")

        # Construcción de la instancia del nuevo registro de Permiso
        permiso = Permiso(
            Activo=True if activo == "1" else False,  # Conversión del string del form a Booleano
            Justificacion=request.POST.get(
                "justificacion"
            ),
            id_TipoPermiso=tipo_permiso,
            idAsistencia=asistencia,
            idEmpleado=empleado
        )

        # Guarda la nueva instancia en la base de datos
        permiso.save()

        # Redirección tras guardar con éxito para evitar el reenvío del formulario (Patrón PRG)
        return redirect(
            'guardar_permiso'
        )

    # ==========================================
    # 3. CONSULTA PARA PANTALLA Y RENDERIZADO (GET)
    # ==========================================

    # Carga de la lista general de permisos registrados con optimización de relaciones JOIN
    permisos = Permiso.objects.select_related(
        'idEmpleado',
        'idEmpleado__idPersona',
        'idAsistencia',
        'id_TipoPermiso'
    )

    # Renderiza la plantilla inyectando todos los catálogos y consultas necesarias
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
# GUARDAR CABECERA DE LA ACCIÓN DEL PERSONAL
# =========================================================
@requiere_permiso("acciones_personal", "crear")  # Restringe la acción a usuarios con permiso de creación
def registrar_cabecera_accion(request, pk=None):
    """
    Gestiona el proceso en 2 pasos de Acciones de Personal:
    Paso 1: Crear o cargar la cabecera (AccionPersonal).
    Paso 2: Registrar el detalle/especificación del movimiento (AccionTipo)
            y actualizar salarios o asignaciones de premios según aplique.
    """
    accion_cabecera = None
    paso_dos_habilitado = False

    # Si se recibe una PK por URL, se busca la cabecera existente y se habilita el paso 2
    if pk:
        accion_cabecera = get_object_or_404(AccionPersonal, pk=pk)
        paso_dos_habilitado = True

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIONES POST
    # -----------------------------------------------------
    if request.method == 'POST':
        action = request.POST.get('action')

        # =================================================
        # FLUJO 1: GUARDAR CABECERA (PASO 1)
        # =================================================
        if action == 'guardar_cabecera':
            form_cabecera = AccionPersonalForm(request.POST)
            
            if form_cabecera.is_valid():
                nueva_cabecera = form_cabecera.save()
                messages.success(
                    request,
                    f"Cabecera guardada con éxito. Folio: {nueva_cabecera.idAccion}"
                )
                # Redirige a la misma vista pasando la PK para activar el Paso 2
                return redirect('gestionar_accion', pk=nueva_cabecera.idAccion)
            else:
                messages.error(request, "Error al validar los datos de la cabecera.")

        # =================================================
        # FLUJO 2: FINALIZAR/SELLAR ACCIÓN (PASO 2)
        # =================================================
        elif action == 'finalizar_accion':
            id_cabecera_padre = request.POST.get('idAccion_padre')
            
            # Validación de integridad: debe existir la cabecera previa
            if not id_cabecera_padre:
                messages.error(request, "Error crítico: No se encontró la cabecera asociada al movimiento.")
                return redirect('crear_accion')

            cabecera_obj = get_object_or_404(AccionPersonal, pk=id_cabecera_padre)
            id_detalle_accion = request.POST.get('Tipo_Accion')
            id_salario_empleado = request.POST.get('idSalario')
            detalle_texto = request.POST.get('Detalle')

            # Validar campos obligatorios de la especificación
            if not id_detalle_accion or not detalle_texto:
                messages.error(request, "Por favor complete todos los campos requeridos de la especificación.")
                return redirect('gestionar_accion', pk=cabecera_obj.idAccion)

            try:
                # Carga de catálogo y objetos relacionados opcionales
                catalogo_accion = get_object_or_404(DetalleAccion, pk=id_detalle_accion)
                
                salario_obj = None
                if id_salario_empleado:
                    salario_obj = get_object_or_404(SalarioEmpleado, pk=id_salario_empleado)

                premio_asignado = None
                id_premio_asignado = request.POST.get("idPremioAsignado")
                if id_premio_asignado:
                    premio_asignado = get_object_or_404(PremioAsignado, pk=id_premio_asignado)

                # --- Lógica de negocio condicional según el tipo de acción ---
                monto = None
                if catalogo_accion.Accion == "Premio":
                    # Asigna el monto capturado para un premio
                    monto = Decimal(request.POST.get("monto_premio"))
                    
                elif catalogo_accion.Accion in ["Ascenso", "Ajuste Salarial"]:
                    # Asigna el nuevo salario e impacta la actualización directa en el registro del empleado
                    monto = Decimal(request.POST.get("nuevo_salario"))
                    if salario_obj:
                        salario_obj.Salario_Sem_Neto = monto
                        salario_obj.save()

                # Registro definitivo del detalle de la acción (AccionTipo)
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

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIÓN GET
    # -----------------------------------------------------
    else:
        # Inicializa el formulario de cabecera (vacío o con instancia para editar/ver)
        form_cabecera = AccionPersonalForm(instance=accion_cabecera)

    # OPTIMIZACIÓN EN PYTHON COMPATIBLE CON CUALQUIER BD (SQLite/MySQL/PostgreSQL):
    # Carga todos los empleados optimizando la relación con Persona
    empleados = Empleado.objects.select_related('idPersona').all()
    
    # Construye un mapa en memoria {idEmpleado: ultimo_salario} recorriendo salarios en orden ascendente
    salarios_recientes = {}
    for s in SalarioEmpleado.objects.order_by('idSalarioEmpleado'):
        salarios_recientes[s.idEmpleado_id] = s.Salario_Sem_Neto

    # Asigna dinámicamente el último salario a cada objeto de empleado en la lista
    for emp in empleados:
        emp.salario_actual = salarios_recientes.get(emp.pk, 0)

    # Construcción del contexto para renderizar la plantilla
    context = {
        'form_cabecera': form_cabecera,
        'accion_cabecera': accion_cabecera,
        'paso_dos_habilitado': paso_dos_habilitado,
        'empleados': empleados,
        'tipos_accion': DetalleAccion.objects.all(),
        'salarios': SalarioEmpleado.objects.all(),
        # Consulta de histórico de acciones optimizada con JOINs multinivel
        'acciones': AccionTipo.objects.select_related(
            'idAccion',
            'id_Detalle_Accion',
            'idAccion__idEmpleado'
        ).order_by('-idAccion_Tipo'),
    }

    return render(request, 'accion_Personal.html', context)


# =========================================================
# GUARDAR DETALLE DE LA ACCIÓN DE PERSONAL
# =========================================================
@requiere_permiso("acciones_personal", "crear")  # Restringe la vista a usuarios con permiso de creación
@transaction.atomic  # Garantiza integridad de la BD: si falla algún paso, revierte (rollback) todas las operaciones escritas
def guardar_accion_tipo(request, id_accion):
    
    # Restringe la ejecución exclusivamente a peticiones POST
    if request.method != "POST":
        return redirect("gestionar_accion")

    # 1. Búsqueda y validación de las instancias base o lanza 404 si no existen
    accion = get_object_or_404(AccionPersonal, pk=id_accion)
    tipo_accion = get_object_or_404(DetalleAccion, pk=request.POST.get("Tipo_Accion"))
    detalle = request.POST.get("Detalle")

    # Instanciación inicial del objeto AccionTipo (Detalle de la acción)
    accion_tipo = AccionTipo(
        idAccion=accion,
        id_Detalle_Accion=tipo_accion,
        Detalle=detalle
    )

    # -----------------------------------------------------
    # LÓGICA DE NEGOCIO CONDICIONAL SEGÚN EL TIPO DE ACCIÓN
    # -----------------------------------------------------

    # Caso A: Modificaciones salariales (Ascenso o Ajuste Salarial)
    if tipo_accion.Accion in ["Ascenso", "Ajuste Salarial"]:
        salario = get_object_or_404(SalarioEmpleado, pk=request.POST.get("idSalarioEmpleado"))
        nuevo_salario = Decimal(request.POST.get("nuevo_salario"))

        # Actualiza e impacta el nuevo salario semanal neto en la tabla de SalarioEmpleado
        salario.Salario_Sem_Neto = nuevo_salario
        salario.save()

        # Vincula la relación del salario y registra el monto actualizado en la acción
        accion_tipo.idSalarioEmpleado = salario
        accion_tipo.Monto_TA = nuevo_salario

    # Caso B: Asignación de Premio
    elif tipo_accion.Accion == "Premio":
        premio = get_object_or_404(PremioAsignado, pk=request.POST.get("idPremioAsignado"))
        
        # Asocia la asignación del premio y registra su monto liquidado correspondiente
        accion_tipo.id_PremioAsignado = premio
        accion_tipo.Monto_TA = premio.Monto_Liquidado

    # 2. Guarda definitivamente el detalle del movimiento en la base de datos
    accion_tipo.save()

    # Notificación de éxito al usuario y redirección al listado/módulo de rotación
    messages.success(request, "La Acción de Personal fue registrada correctamente.")
    return redirect("accion_rotacion")


# =========================================================
# OBTENER SALARIO ACTUAL DEL EMPLEADO (AJAX)
# =========================================================
@requiere_permiso("acciones_personal", "ver")  # Exige permiso de lectura en 'acciones_personal' para consultar la API
def obtener_salario_empleado(request):
    """
    Endpoint para solicitudes asíncronas (AJAX).
    Recibe el ID de un empleado vía GET y retorna en JSON su último
    salario semanal neto registrado en el sistema.
    """
    # 1. Obtención del parámetro 'idEmpleado' enviado desde la petición JavaScript
    id_empleado = request.GET.get("idEmpleado")

    # 2. Búsqueda del último registro salarial del empleado
    # Se ordena descendentemente por ID (-idSalarioEmpleado) y se toma el primero (.first())
    salario = SalarioEmpleado.objects.filter(
        idEmpleado=id_empleado
    ).order_by("-idSalarioEmpleado").first()

    # 3. Construcción y retorno de la respuesta en formato JSON
    if salario:
        # Caso de éxito: Retorna confirmación, ID del registro salarial y el monto convertido a float
        return JsonResponse({
            "success": True,
            "idSalarioEmpleado": salario.idSalarioEmpleado,
            "salario": float(salario.Salario_Sem_Neto)
        })

    # Caso alternativo: El empleado no cuenta con registros salariales asociados en la BD
    return JsonResponse({
        "success": False,
        "mensaje": "El empleado no posee salario registrado."
    })


# =========================================================
# OBTENER PREMIO DEL EMPLEADO (AJAX)
# =========================================================
@requiere_permiso("acciones_personal", "ver")  # Requiere permiso de lectura en el módulo 'acciones_personal'
def obtener_premio_empleado(request):
    """
    Endpoint para solicitudes asíncronas (AJAX).
    Recibe el ID de un empleado vía GET y consulta a través de la relación de su KPI
    el último premio asignado, retornando sus detalles en formato JSON.
    """
    # 1. Captura del ID del empleado enviado mediante parámetros Query String en GET
    id_empleado = request.GET.get("idEmpleado")

    # 2. Consulta a la BD filtrando por el empleado asociado al KPI
    # - Realiza la búsqueda a través de la relación inversa 'id_KPI__idEmpleado'
    # - Optimiza con select_related('idPremio') para obtener la descripción sin consultas adicionales
    # - Ordena por fecha de registro descendente para traer la asignación más reciente
    premio = PremioAsignado.objects.filter(
        id_KPI__idEmpleado=id_empleado
    ).select_related("idPremio").order_by("-Fecha_Registro").first()

    # 3. Construcción y retorno de la respuesta JSON
    if premio:
        # Caso exitoso: Retorna datos del premio (ID asignación, monto liquidado y descripción)
        return JsonResponse({
            "success": True,
            "idPremioAsignado": premio.id_PremioAsignado,
            "monto": float(premio.Monto_Liquidado),
            "descripcion": premio.idPremio.Descripcion
        })

    # Caso en que el empleado no tenga ningún premio vinculado en su historial
    return JsonResponse({
        "success": False,
        "mensaje": "El empleado no posee premios registrados."
    })



# =========================================================
# ROTACIÓN DE PERSONAL
# =========================================================
@requiere_permiso("acciones_personal", "ver")  # Normalizado al slug 'acciones_personal'
def rotacion_personal(request):
    """
    Calcula los indicadores de rotación de personal (IRP) en un período (Año/Mes) 
    a partir de las contrataciones (Onboarding), bajas (Offboarding) y plantilla inicial/final.
    Permite previsualizar los resultados o guardarlos en el historial acumulado.
    """
    data_calculada = {}
    registro = {}

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIONES POST (CÁLCULO Y GUARDADO)
    # -----------------------------------------------------
    if request.method == "POST":
        action = request.POST.get("action")
        
        # Extracción y casteo del período a evaluar
        anio = int(request.POST.get("Anio"))
        mes = request.POST.get("Mes")
        mes = int(mes) if mes else None

        # -------------------------------------------------
        # 1. CONTRATACIONES (ONBOARDING)
        # -------------------------------------------------
        contratados = Onboarding.objects.filter(Fecha_Inicio__year=anio)
        if mes:
            contratados = contratados.filter(Fecha_Inicio__month=mes)
        A_Contratados = contratados.count()

        # -------------------------------------------------
        # 2. DESVINCULACIONES / BAJAS (OFFBOARDING)
        # -------------------------------------------------
        desvinculados = Offboarding.objects.filter(Fecha_Salida__year=anio)
        if mes:
            desvinculados = desvinculados.filter(Fecha_Salida__month=mes)

        # Bajas regulares (excluye salidas por retiro o fuerza mayor)
        D_Desvinculados = desvinculados.exclude(
            idCausa__Categoria__in=["Retiro", "Fuerza Mayor"]
        ).count()

        # Bajas no atribuibles a rotación voluntaria/operativa (Jubilaciones o Defunciones)
        D_Jubilaciones_Defuncionales = desvinculados.filter(
            idCausa__Categoria__in=["Retiro", "Fuerza Mayor"]
        ).count()

        # Sumatoria total de bajas en el período
        D_Total_Bajas = D_Desvinculados + D_Jubilaciones_Defuncionales

        # -------------------------------------------------
        # 3. PERSONAL INICIAL (PLANTILLA BASE)
        # -------------------------------------------------
        if mes:
            # Empleados contratados antes del primer día del mes en evaluación y activos
            empleados_inicio = Empleado.objects.filter(
                Fecha_Ingreso__lt=f"{anio}-{mes:02d}-01",
                Activo=True
            ).count()
        else:
            # Empleados contratados en años anteriores al año evaluado y activos
            empleados_inicio = Empleado.objects.filter(
                Fecha_Ingreso__year__lt=anio,
                Activo=True
            ).count()

        # -------------------------------------------------
        # 4. FÓRMULA DEL ÍNDICE DE ROTACIÓN DE PERSONAL (IRP)
        # -------------------------------------------------
        F1_Inicio = empleados_inicio
        # Balance final = Inicio + Altas - Bajas
        F2_Final = F1_Inicio + A_Contratados - D_Total_Bajas
        promedio = (F1_Inicio + F2_Final) / 2

        # Cálculo porcentual del IRP frente a la plantilla promedio
        if promedio > 0:
            IRP = round((D_Total_Bajas / promedio) * 100, 2)
        else:
            IRP = Decimal("0.00")

        # Umbrales o rangos objetivo sugeridos para el indicador IRP
        IRP_Sugerido_Min = Decimal("1.00")
        IRP_Sugerido_Max = Decimal("4.00")

        # Mapeo del diccionario con las métricas calculadas
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

        # Datos del formulario para mantener la selección en el frontend
        registro = {"Anio": anio, "Mes": mes}

        # -------------------------------------------------
        # 5. GUARDAR REGISTRO EN EL HISTORIAL
        # -------------------------------------------------
        if action == "guardar":
            try:
                # Crea la tupla del período consolidado en la BD
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
                # Captura violaciones de unicidad si el período (Año/Mes) ya había sido guardado previa o incorrectamente
                messages.error(request, str(e))

    # -----------------------------------------------------
    # PROCESAMIENTO GET Y RENDERIZADO DE PANTALLA
    # -----------------------------------------------------
    context = {
        "registro": registro,
        "data_calculada": data_calculada,
        # Carga el histórico guardado ordenando cronológicamente de forma descendente
        "historial": RotacionPersonal.objects.order_by("-Anio", "-Mes")
    }

    return render(request, "rotacion_Personal.html", context)



def evaluaciones_view(request):
    return render(request, 'evaluaciones.html')


# =========================================================
# CREAR EVALUACIÓN + DESEMPEÑO (CABECERA + DETALLE)
# =========================================================
@requiere_permiso("evaluaciones", "ver")  # Exige permiso de lectura inicial para cargar el formulario
def crear_evaluacion(request):
    """
    Gestiona el registro completo de una evaluación de desempeño.
    Crea tanto la cabecera (Evaluacion) como el detalle con sus criterios 
    y porcentaje final (EvaluacionDesempeno) dentro de una transacción atómica.
    """
    # Consulta de catálogos necesarios para los desplegables de la plantilla
    # Optimiza las relaciones con Persona mediante select_related
    empleados = Empleado.objects.select_related("idPersona").all()
    evaluadores = Empleado.objects.select_related("idPersona").all()
    periodos = Periodo.objects.all()

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIÓN POST (GUARDAR REGISTRO)
    # -----------------------------------------------------
    if request.method == "POST":

        # Validación secundaria/específica de permisos de escritura (Creación)
        bloqueo = bloquear_si_no_puede(
            request,
            "evaluacion_desempeno",
            "crear"
        )

        if bloqueo:
            return bloqueo

        try:
            # Garantiza que la cabecera y el detalle se guarden juntos; 
            # si falla uno, se revierte toda la operación (rollback)
            with transaction.atomic():

                # ============================
                # 1. CABECERA (Evaluacion)
                # ============================
                idEmpleado = request.POST.get("idEmpleado")
                idEvaluador = request.POST.get("idEvaluador")
                fecha = request.POST.get("Fecha_Evaluacion")
                periodo_id = request.POST.get("periodo")

                # Creación del registro principal/cabecera
                evaluacion = Evaluacion.objects.create(
                    Fecha_Evaluacion=fecha,
                    idPeriodo_id=periodo_id,
                    idEmpleado_Ev_id=idEmpleado,  # ID del empleado evaluado
                    idEmpleado_Jef_id=idEvaluador # ID del jefe/evaluador
                )

                # ============================
                # 2. DETALLE (EvaluacionDesempeno)
                # ============================
                # Conversión de valores del formulario HTML ('1' o '0') a booleanos (True/False)
                c1 = request.POST.get("Cumple_Metas_Objetivos") == "1"
                c2 = request.POST.get("Cumple_FuncionesAsig") == "1"
                c3 = request.POST.get("Entregables_Calidad_Tiempo") == "1"
                c4 = request.POST.get("Cumple_Asistencia") == "1"
                c5 = request.POST.get("Muestra_Compromiso_Colaboracion") == "1"

                # Sumatoria de criterios cumplidos (los booleanos suman True=1, False=0)
                total = sum([c1, c2, c3, c4, c5])

                # Cálculo del porcentaje final asignado (Escala sobre 5 criterios = 100%)
                pct_total = (total / 5) * 100

                observaciones = request.POST.get(
                    "Observaciones",
                    ""
                )

                # Creación del detalle de desempeño asociado a la cabecera recién creada
                EvaluacionDesempeno.objects.create(
                    cumple_metas_objetivos=c1,
                    cumple_funciones_asig=c2,
                    entregables_calidad_tiempo=c3,
                    cumple_asistencia=c4,
                    muestra_compromiso_colaboracion=c5,
                    pct_total_ev=pct_total,
                    observaciones=observaciones,
                    evaluacion=evaluacion  # Asocia la FK del objeto de cabecera
                )

                messages.success(
                    request,
                    "Evaluación registrada correctamente."
                )

                return redirect("crear_evaluacion")

        except Exception as e:
            # Captura y despliega cualquier error ocurrido durante la transacción
            messages.error(
                request,
                f"Error al guardar: {str(e)}"
            )

    # -----------------------------------------------------
    # PROCESAMIENTO GET Y RENDERIZADO
    # -----------------------------------------------------
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
@requiere_permiso("evaluaciones", "ver")  # Permiso previo para visualizar la vista de evaluaciones
def crear_evaluacion_jefatura(request):
    """
    Vista encargada de procesar el registro de la evaluación de potencial por jefatura.
    
    Flujo de ejecución:
    1. Carga los catálogos de Empleados, Evaluadores y Periodos.
    2. Si la petición es POST:
       a. Verifica los permisos de escritura ('crear') específicos para 'evaluacion_jefatura'.
       b. Inicia un bloque transaccional atómico (`transaction.atomic()`).
       c. Crea el registro principal en la tabla `Evaluacion` (Cabecera).
       d. Procesa las 5 competencias cualitativas a valores booleanos y calcula el porcentaje ponderado.
       e. Crea el detalle en la tabla `EvaluacionJefePotencial`.
       f. Muestra un mensaje flash de éxito y redirige a la misma vista (Patrón PRG).
    3. Si la petición es GET (o falla el proceso):
       a. Renderiza el plantilla `eva_Jefatura.html` pasándole los catálogos en el contexto.
    """

    # 1. Carga de catálogos base para popular los selectores desplegables de la plantilla HTML
    # Se utiliza select_related("idPersona") para optimizar las consultas SQL (evita el problema N+1)
    empleados = Empleado.objects.select_related("idPersona").all()
    evaluadores = Empleado.objects.select_related("idPersona").all()
    periodos = Periodo.objects.all()

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIÓN POST (CREAR EVALUACIÓN)
    # -----------------------------------------------------
    if request.method == "POST":

        # Validar en tiempo de ejecución si el usuario tiene permiso explícito de creación
        bloqueo = bloquear_si_no_puede(
            request,
            "evaluacion_jefatura",
            "crear"
        )

        if bloqueo:
            return bloqueo  # Interrumpe el flujo y retorna la respuesta de bloqueo (p. ej., 403 Forbidden o redirección)

        try:
            # Transacción Atómica: Si ocurre cualquier excepción en este bloque, 
            # la base de datos revierte automáticamente los cambios (Rollback)
            with transaction.atomic():

                # ====================================
                # 1. REGISTRO DE LA CABECERA (Evaluacion)
                # ====================================
                idEmpleado = request.POST.get("idEmpleado")
                idEvaluador = request.POST.get("idEvaluador")
                fecha = request.POST.get("Fecha_Evaluacion")
                periodo_id = request.POST.get("periodo")

                # Inserción en la tabla padre (Cabecera general de la evaluación)
                evaluacion = Evaluacion.objects.create(
                    Fecha_Evaluacion=fecha,
                    idPeriodo_id=periodo_id,
                    idEmpleado_Ev_id=idEmpleado,  # Clave foránea del empleado evaluado
                    idEmpleado_Jef_id=idEvaluador # Clave foránea de la jefatura / evaluador
                )

                # ====================================
                # 2. DETALLE DE POTENCIAL (EvaluacionJefePotencial)
                # ====================================
                # Conversión de las entradas del formulario ('1' o '0') a tipos de datos Booleanos (True/False)
                liderazgo = request.POST.get("Capacidad_Liderazgo") == "1"
                aprendizaje = request.POST.get("Aprendizaje_Rapido") == "1"
                adaptacion = request.POST.get("Adaptacion_Cambio") == "1"
                iniciativa = request.POST.get("Iniciativa_Mejora") == "1"
                madurez = request.POST.get("Madurez_Emocional") == "1"

                observaciones = request.POST.get("Observaciones", "")

                # Sumatoria de competencias cumplidas
                # En Python: True se evalúa como 1 y False como 0
                total = sum([
                    liderazgo,
                    aprendizaje,
                    adaptacion,
                    iniciativa,
                    madurez
                ])

                # Cálculo del porcentaje ponderado (Cada competencia equivale al 20% del total)
                pct_total = (total / 5) * 100

                # Inserción en la tabla hija (Detalle específico de la evaluación por jefatura)
                EvaluacionJefePotencial.objects.create(
                    Capacidad_Liderazgo=liderazgo,
                    Aprendizaje_Rapido=aprendizaje,
                    Adaptacion_Cambio=adaptacion,
                    Iniciativa_Mejora=iniciativa,
                    Madurez_Emocional=madurez,
                    pct_totalEv=pct_total,
                    Observaciones=observaciones,
                    idEvaluacion=evaluacion  # Asignación del objeto cabecera recién creado
                )

                # Notificación exitosa mediante el framework de mensajes de Django
                messages.success(
                    request,
                    "Evaluación de jefatura registrada correctamente."
                )

                # Redirección tras guardar con éxito (evita el reenvío duplicado de formularios al refrescar)
                return redirect("crear_evaluacion_jefatura")

        except Exception as e:
            # Captura cualquier falla durante la transacción (ej. campos nulos, error de integridad)
            messages.error(
                request,
                f"Error al guardar: {str(e)}"
            )

    # -----------------------------------------------------
    # RENDERIZADO DE PANTALLA (PETICIONES GET O CON ERRORES)
    # -----------------------------------------------------
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
@requiere_permiso("evaluaciones", "crear")  # Restringe la vista a usuarios con permisos de creación en 'evaluaciones'
def crear_matriz_9box(request):
    """
    Gestiona el registro de la clasificación de un empleado en la Matriz 9 Box (Talento vs. Desempeño).
    Carga todos los catálogos paramétricos necesarios para definir el cuadrante, perfil, desempeño, 
    potencial y plan de acción asociado.
    """
    # 1. Carga de catálogos base para popular los selectores de la plantilla HTML
    # Optimiza la relación de empleados con Persona usando select_related
    empleados = Empleado.objects.select_related("idPersona").all()
    periodos = Periodo.objects.all()
    perfiles = Cuadrante9BoxPerfil.objects.all()
    cuadrantes = Cuadrante9Box.objects.all()
    desempenos = Cuadrante9BoxDesempeno.objects.all()
    potenciales = Cuadrante9BoxPotencial.objects.all()

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIÓN POST (CREAR REGISTRO)
    # -----------------------------------------------------
    if request.method == "POST":

        # Validación explicita en tiempo de ejecución para permisos de escritura
        bloqueo = bloquear_si_no_puede(
            request,
            "evaluaciones",
            "crear"
        )

        if bloqueo:
            return bloqueo  # Retorna la respuesta de restricción de acceso

        try:
            # Garantiza la integridad referencial al guardar la asignación
            with transaction.atomic():

                # Inserción en la tabla de unión de la matriz 9 Box con las claves foráneas enviadas
                UnionMatrizEmp.objects.create(
                    Anio=request.POST.get("Anio"),
                    Plan_Accion=request.POST.get("Plan_Accion"),
                    idPeriodo_id=request.POST.get("periodo"),
                    idCuadrante_9box_id=request.POST.get("idCuadrante_9box"),
                    idCuadrante_9box_Perfil_id=request.POST.get("idCuadrante_9box_Perfil"),
                    idCuadrante_9box_Desempeno_id=request.POST.get("idCuadrante_9box_Desempeno"),
                    idCuadrante_9box_Potencial_id=request.POST.get("idCuadrante_9box_Potencial"),
                    idEmpleado_id=request.POST.get("idEmpleado")
                )

                messages.success(
                    request,
                    "Matriz 9 Box registrada correctamente."
                )

                # Redirección tras guardado exitoso (Patrón PRG para evitar re-envío de formularios)
                return redirect("crear_matriz_9box")

        except Exception as e:
            # Captura de excepciones en caso de inconsistencia o fallo al guardar
            messages.error(
                request,
                f"Error al guardar: {str(e)}"
            )

    # -----------------------------------------------------
    # RENDERIZADO DE PANTALLA (PETICIONES GET O CON ERRORES)
    # -----------------------------------------------------
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
@requiere_permiso("evaluaciones", "ver")  # Exige permiso de lectura en el módulo 'evaluaciones'
def dashboard_resultados(request):
    """
    Consolida y visualiza los resultados de evaluación de un empleado para un período y año específicos.
    
    Flujo de consulta:
    1. Obtiene los catálogos para filtros (Empleados y Períodos).
    2. Lee los parámetros GET enviados desde el formulario de búsqueda.
    3. Si existen los tres filtros (empleado, período y año):
       a. Consulta la matriz 9 Box (`UnionMatrizEmp`) con optimización de relaciones (`select_related`).
       b. Si existe la matriz, busca la evaluación de cabecera más reciente.
       c. Intenta obtener primero el detalle de desempeño (`EvaluacionDesempeno`).
       d. Si no hay desempeño, busca como alternativa el detalle de potencial (`EvaluacionJefePotencial`).
       e. Extrae el porcentaje correspondiente y define la etiqueta adecuada para el dashboard.
    4. Mantiene el estado de los filtros para conservarlos en el frontend (plantilla).
    """

    # 1. Carga de catálogos base para los filtros desplegables de la plantilla HTML
    # Uso de select_related para evitar el problema N+1 al cargar las personas asociadas
    empleados = Empleado.objects.select_related(
        "idPersona"
    ).all()

    periodos = Periodo.objects.all()

    # 2. Captura de parámetros GET enviados desde la barra o formulario de filtros
    empleado_filtro = request.GET.get(
        "empleado_filtro"
    )

    periodo_filtro = request.GET.get(
        "periodo_filtro"
    )

    anio_filtro = request.GET.get(
        "anio_filtro"
    )

    # Inicialización de variables para la vista/contexto
    matriz_seleccionada = None
    potencial_seleccionado = None
    desempeno_seleccionado = None

    porcentaje_total = 0
    titulo_porcentaje = "Sin evaluación"

    # 3. Procesamiento de consulta solo si se envían los 3 parámetros obligatorios
    if empleado_filtro and periodo_filtro and anio_filtro:

        try:
            # Consulta optimizada de la asignación en la Matriz 9 Box
            # Carga de forma anticipada (JOIN) las tablas relacionadas requeridas en el dashboard
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
                # Notificación en caso de que no haya registro en la matriz con los filtros dados
                messages.warning(
                    request,
                    "No se encontraron resultados para los criterios seleccionados."
                )

            else:
                # Si existe matriz, busca la cabecera de evaluación correspondiente al empleado y período
                # Ordena descendente por fecha para obtener la más reciente
                evaluacion = Evaluacion.objects.filter(
                    idEmpleado_Ev_id=empleado_filtro,
                    idPeriodo_id=periodo_filtro
                ).order_by(
                    "-Fecha_Evaluacion"
                ).first()

                if evaluacion:
                    # Intenta obtener el detalle de Evaluación de Desempeño
                    desempeno_seleccionado = (
                        EvaluacionDesempeno.objects.filter(
                            evaluacion=evaluacion
                        ).first()
                    )

                    if desempeno_seleccionado:
                        # Asigna el porcentaje y título de Desempeño si existe el registro
                        porcentaje_total = (
                            desempeno_seleccionado.pct_total_ev or 0
                        )

                        titulo_porcentaje = (
                            "Porcentaje de Desempeño"
                        )

                    else:
                        # Si no hay registro de desempeño, busca el detalle de Evaluación de Potencial (Jefatura)
                        potencial_seleccionado = (
                            EvaluacionJefePotencial.objects.filter(
                                idEvaluacion=evaluacion
                            ).first()
                        )

                        if potencial_seleccionado:
                            # Asigna el porcentaje y título de Potencial si existe el registro
                            porcentaje_total = (
                                potencial_seleccionado.pct_totalEv or 0
                            )

                            titulo_porcentaje = (
                                "Porcentaje Potencial (Jefatura)"
                            )

        except Exception as e:
            # Captura de errores inesperados durante la ejecución de las consultas SQL
            messages.error(
                request,
                f"Error al consultar los datos: {str(e)}"
            )

    # 4. Construcción del contexto para el renderizado del template
    context = {
        "empleados": empleados,
        "periodos": periodos,
        "matriz_seleccionada": matriz_seleccionada,
        "potencial_seleccionado": potencial_seleccionado,
        "desempeno_seleccionado": desempeno_seleccionado,
        "porcentaje_total": porcentaje_total,
        "titulo_porcentaje": titulo_porcentaje,

        # Conversión/mantenimiento de valores filtrados para rellenar/mantener el formulario en el frontend
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
@requiere_permiso("kpi", "crear")  # Garantiza que el usuario tenga permisos de creación en el módulo 'kpi'
def registrar_kpi_view(request):
    """
    Gestiona la carga inicial y la creación de la cabecera para la evaluación de KPIs.
    
    Flujo de ejecución:
    1. Inicializa variables de estado y valores por defecto (Año 2026).
    2. Si la petición es POST:
       a. Valida los permisos de escritura del usuario.
       b. Captura y castea los parámetros enviados (`idEmpleado`, `Mes`, `Anio`).
       c. Intenta recuperar el objeto `Empleado` e instanciar/guardar `KpiCabecera`.
       d. Captura excepciones específicas (duplicidad por restricción `unique_together`, empleado inexistente, o datos corruptos).
    3. Carga la lista de empleados activos y categorías de KPI para los selectores.
    4. Renderiza la plantilla `kpi_Registro.html` manteniendo el estado de la cabecera creada o seleccionada.
    """

    # Inicialización de variables para el contexto del template
    kpi_cabecera_id = None
    el_empleado_seleccionado = ""
    el_mes_seleccionado = ""
    el_anio_seleccionado = "2026"  # Valor predeterminado para el año en curso

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIÓN POST (GUARDAR CABECERA)
    # -----------------------------------------------------
    if request.method == 'POST':

        # Validar en tiempo de ejecución si el usuario tiene permiso para crear KPI
        bloqueo = bloquear_si_no_puede(
            request,
            "kpi",
            "crear"
        )

        if bloqueo:
            return bloqueo  # Corta el flujo y retorna la respuesta de acceso denegado

        # Captura de datos enviados desde el formulario POST
        id_empleado = request.POST.get('idEmpleado')
        mes = request.POST.get('Mes')
        anio = request.POST.get('Anio')

        # Conversión de valores a enteros para mantener la selección activa en los selectores HTML
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
            # Obtención de la instancia del empleado
            empleado = Empleado.objects.get(
                pk=id_empleado
            )

            # Instanciación de la cabecera del KPI
            cabecera = KpiCabecera(
                idEmpleado=empleado,
                mes=int(mes),
                anio=int(anio)
            )

            # Inserción en la base de datos
            cabecera.save()

            # Captura del ID primario autogenerado para habilitar el registro de detalles
            kpi_cabecera_id = cabecera.id_KPI

            messages.success(
                request,
                f"¡Cabecera registrada con éxito! ID Asignado: {kpi_cabecera_id}"
            )

        except IntegrityError:
            # Se dispara si ya existe un registro con la combinación única (Empleado + Mes + Año)
            messages.error(
                request,
                "Error: Ya existe un registro de KPI para este colaborador en el mes y año seleccionados."
            )

        except Empleado.DoesNotExist:
            # Manejo de error si la clave primaria del empleado enviada no existe
            messages.error(
                request,
                "El colaborador seleccionado no es válido."
            )

        except (ValueError, TypeError):
            # Manejo de fallos en la conversión de tipos (ej. envío de texto no numérico en mes/año)
            messages.error(
                request,
                "Error: Los datos de mes o año enviados no son válidos."
            )

    # -----------------------------------------------------
    # CARGA DE CATÁLOGOS Y RENDERIZADO (GET / POST)
    # -----------------------------------------------------
    # Carga únicamente los empleados en estado Activo para el selector
    empleados = Empleado.objects.filter(
        Activo=True
    )

    categorias = KpiCategoria.objects.all()

    # Construcción del contexto para el template
    context = {
        'empleados': empleados,
        'categorias': categorias,
        'kpi_cabecera_id': kpi_cabecera_id,  # Si no es None, habilita el formulario de detalles en el frontend
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
@requiere_permiso("kpi", "crear")  # Restringe la ejecución a usuarios con permiso de creación en 'kpi'
def registrar_kpi_detalle_view(request):
    """
    Procesa de manera independiente la adición de una línea de detalle (indicador específico)
    asociada a una cabecera de KPI existente.
    
    Flujo de ejecución:
    1. Verifica que la solicitud sea POST (procesamiento de formulario).
    2. Valida los permisos de escritura del usuario en tiempo de ejecución.
    3. Captura los datos del formulario (`id_KPI`, `id_KPI_Categoria`, `pct_Alcanzado`, `Monto_Base`).
    4. Obtiene los objetos correspondientes mediante `get_object_or_404`.
    5. Calcula el `Monto_Total` alcanzado con base en el porcentaje y el monto base.
    6. Crea y guarda la instancia de `KpiDetalle` (con redondeo a 2 decimales).
    7. Redirige a la vista principal de registro (`registrar_kpi`).
    """

    if request.method == 'POST':

        # Validar en tiempo de ejecución si el usuario tiene permiso para crear detalles de KPI
        bloqueo = bloquear_si_no_puede(
            request,
            "kpi",
            "crear"
        )

        if bloqueo:
            return bloqueo  # Corta el flujo y retorna la respuesta de restricción de acceso

        # Captura de los valores enviados por el formulario POST
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
            # Recupera la cabecera padre existente; si no existe, lanza un error HTTP 404
            cabecera = get_object_or_404(
                KpiCabecera,
                pk=id_kpi_cabecera
            )

            # Recupera la categoría/indicador a evaluar; si no existe, lanza un error HTTP 404
            categoria = get_object_or_404(
                KpiCategoria,
                pk=id_categoria
            )

            # Cálculo en memoria del monto alcanzado según el porcentaje (Ej: Monto_Base * (85.0 / 100))
            monto_total = (
                float(monto_base)
                *
                (
                    float(pct_alcanzado) / 100.0
                )
            )

            # Creación e instanciación del objeto de detalle con casting numérico explicito
            detalle = KpiDetalle(
                id_KPI=cabecera,                       # Clave foránea a la cabecera
                id_KPI_Categoria=categoria,           # Clave foránea a la categoría
                pct_Alcanzado=float(
                    pct_alcanzado
                ),
                Monto_Base=float(
                    monto_base
                ),
                Monto_Total=round(
                    monto_total,
                    2                                  # Redondeo del resultado a 2 decimales
                )
            )

            # Inserción en la base de datos
            detalle.save()

            messages.success(
                request,
                f"Indicador '{categoria.tipo_categoria}' añadido exitosamente."
            )

        except IntegrityError:
            # Captura violación de restricción única (ej. prevenir duplicados de una misma categoría en la misma cabecera)
            messages.error(
                request,
                "Error: Esta categoría ya fue evaluada en este mes para el colaborador."
            )

        except Exception as e:
            # Captura de errores inesperados (ej. fallos en la conversión a float o tipos incompatibles)
            messages.error(
                request,
                f"Error al guardar el detalle: {str(e)}"
            )

    # Redirección final mediante el patrón Post/Redirect/Get hacia la vista principal de registro
    return redirect(
        'registrar_kpi'
    )


# =========================================================
# CREAR PREMIO
# =========================================================
@requiere_permiso("kpi", "crear")  # Garantiza que el usuario posea permisos de creación en el módulo 'kpi'
def crear_premio(request):
    """
    Gestiona la creación de nuevos premios vinculados a las categorías de KPI y perfiles de la Matriz 9 Box,
    además de obtener el listado histórico de los premios registrados.
    
    Flujo de ejecución:
    1. Si la petición es POST:
       a. Verifica los permisos de escritura del usuario en tiempo de ejecución.
       b. Instancia el formulario `PremioForm` con la información enviada.
       c. Si el formulario es válido, guarda el nuevo registro, emite un mensaje de éxito y redirige (Patrón PRG).
    2. Si la petición es GET:
       a. Instancia un formulario `PremioForm` vacío listo para ser renderizado.
    3. Carga la lista completa de premios optimizando la consulta con `select_related`.
    4. Renderiza la plantilla `kpi_Premio.html` pasando el formulario y la colección de premios en el contexto.
    """

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIÓN POST (CREACIÓN DE PREMIO)
    # -----------------------------------------------------
    if request.method == 'POST':

        # Validar en tiempo de ejecución si el usuario tiene permiso explícito para crear premios
        bloqueo = bloquear_si_no_puede(
            request,
            "kpi",
            "crear"
        )

        if bloqueo:
            return bloqueo  # Interrumpe el flujo y retorna la respuesta de restricción de acceso

        # Instancia el formulario con los datos recibidos en la solicitud POST
        form = PremioForm(
            request.POST
        )

        # Validación del formulario (comprueba reglas del Modelo y tipado de campos)
        if form.is_valid():

            # Guarda la nueva instancia del modelo Premio en la base de datos
            form.save()

            messages.success(
                request,
                '¡Premio guardado exitosamente!'
            )

            # Redirección tras éxito para limpiar el formulario y evitar el reenvío de datos (Patrón PRG)
            return redirect(
                'crear_premio'
            )

    # -----------------------------------------------------
    # PROCESAMIENTO DE PETICIÓN GET (CARGA INICIAL)
    # -----------------------------------------------------
    else:
        # Crea una instancia vacía del formulario para su presentación inicial en el HTML
        form = PremioForm()

    # -----------------------------------------------------
    # CONSULTA Y RENDERIZADO DE LA PLANTILLA
    # -----------------------------------------------------
    # Consulta optimizada mediante JOINs explícitos (select_related) para cargar
    # la categoría de KPI y el perfil 9 Box asociados a cada premio sin generar consultas N+1
    premios = Premio.objects.select_related(
        'id_KPI_Categoria',
        'idCuadrante_9box_Perfil'
    ).all().order_by(
        'idPremio'
    )

    # Renderiza la vista 'kpi_Premio.html' enviando el formulario (lleno con errores o vacío) y los registros
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
# Decorador personalizado para restringir el acceso a la vista.
# Requiere que el usuario tenga el permiso de "crear" dentro del módulo "kpi".
@requiere_permiso("kpi", "crear")
def guardar_premio_asignado(request):

    # =====================================================
    # MÉTODO POST: PROCESAMIENTO DEL FORMULARIO
    # =====================================================
    # Se evalúa si el navegador/cliente envió una solicitud de tipo POST (envío de datos).
    if request.method == 'POST':

        # Verificación explícita de seguridad adicional.
        # Si el usuario no cumple los criterios, 'bloquear_si_no_puede' retorna una respuesta de bloqueo/redirección.
        bloqueo = bloquear_si_no_puede(
            request,
            "kpi",
            "crear"
        )

        # Si existe una respuesta de bloqueo, se interrumpe la ejecución y se devuelve dicha respuesta.
        if bloqueo:
            return bloqueo

        # =================================================
        # CREAR FORMULARIO CON LOS DATOS RECIBIDOS
        # =================================================
        # Se vinculan los datos ingresados en el formulario (request.POST) con la clase PremioAsignadoForm.
        form = PremioAsignadoForm(
            request.POST
        )

        # =================================================
        # VALIDAR FORMULARIO
        # =================================================
        # Ejecuta las validaciones del formulario. Si todos los campos son válidos, accede a 'cleaned_data'.
        if form.is_valid():

            try:
                # Se utiliza una transacción atómica para garantizar que todas las operaciones dentro
                # del bloque se ejecuten correctamente o se reviertan (rollback) si ocurre algún error.
                with transaction.atomic():

                    # Extracción de campos validados desde el diccionario cleaned_data
                    premio = (
                        form.cleaned_data['idPremio']
                    )

                    kpi = (
                        form.cleaned_data['id_KPI']
                    )

                    fecha_registro = (
                        form.cleaned_data['Fecha_Registro']
                    )

                    # =================================================
                    # VALIDACIÓN DE NEGOCIO: EXISTENCIA DEL DETALLE KPI
                    # =================================================
                    # Se busca si el KPI seleccionado posee un detalle asignado que coincida 
                    # con la misma categoría asociada al premio.
                    detalle_kpi = (
                        KpiDetalle.objects.filter(
                            id_KPI=kpi,
                            id_KPI_Categoria=premio.id_KPI_Categoria
                        ).first()
                    )

                    # Si no existe coincidencia entre el KPI y la categoría del premio:
                    if detalle_kpi is None:

                        # Se envía un mensaje de error al usuario informando la inconsistencia.
                        messages.error(
                            request,
                            'No se puede asignar este premio. '
                            'El KPI seleccionado no tiene un '
                            'detalle registrado para la categoría '
                            'asociada al premio.'
                        )

                        # Se vuelve a renderizar el formulario con sus datos actuales y la lista de premios actualizados.
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

                    # =================================================
                    # REGISTRO Y GUARDADO DE LA ASIGNACIÓN
                    # =================================================
                    # Instancia del modelo PremioAsignado con los datos recibidos del formulario.
                    premio_asignado = PremioAsignado(
                        Fecha_Registro=fecha_registro,
                        idPremio=premio,
                        id_KPI=kpi
                    )

                    # Guarda el objeto en la base de datos (aquí se pueden ejecutar signals o reglas del modelo).
                    premio_asignado.save()

                    # Mensaje de confirmación que incluye el monto calculado o procesado.
                    messages.success(
                        request,
                        (
                            'El premio fue asignado correctamente. '
                            f'Monto liquidado: '
                            f'{premio_asignado.Monto_Liquidado}'
                        )
                    )

                    # Redirección mediante el patrón Post/Redirect/Get para prevenir reenvíos dobles del formulario.
                    return redirect(
                        'guardar_premio_asignado'
                    )

            # =================================================
            # MANEJO DE EXCEPCIONES
            # =================================================
            # Captura errores relacionados con restricciones de clave única, foráneas o de base de datos.
            except IntegrityError as e:

                print(
                    'ERROR DE INTEGRIDAD AL GUARDAR PREMIO ASIGNADO:',
                    str(e)
                )

                messages.error(
                    request,
                    (
                        'No fue posible guardar el premio asignado. '
                        'Verifique que los datos seleccionados sean válidos.'
                    )
                )

            # Captura errores de valor lanzados por la lógica del modelo o métodos de validación.
            except ValueError as e:

                print(
                    'ERROR DE VALIDACIÓN AL GUARDAR PREMIO ASIGNADO:',
                    str(e)
                )

                messages.error(
                    request,
                    str(e)
                )

            # Captura cualquier otro tipo de error no controlado previamente.
            except Exception as e:

                print(
                    'ERROR INESPERADO AL GUARDAR PREMIO ASIGNADO:',
                    str(e)
                )

                messages.error(
                    request,
                    (
                        'Ocurrió un error inesperado al guardar '
                        'el premio asignado.'
                    )
                )

        # Si form.is_valid() retorna False, se notifica que hay errores de entrada.
        else:
            messages.error(
                request,
                (
                    'Por favor, revise los datos ingresados '
                    'en el formulario.'
                )
            )

    # =====================================================
    # MÉTODO GET: CARGA INICIAL DE LA VISTA
    # =====================================================
    # Si la petición no es POST, se genera una instancia vacía del formulario para crear un nuevo registro.
    else:

        form = PremioAsignadoForm()

    # =====================================================
    # RENDERIZADO DE LA PLANTILLA (GET o POST con error)
    # =====================================================
    # Se renderiza la plantilla HTML enviando el formulario y el historial de premios asignados.
    # 'select_related' optimiza la consulta SQL realizando JOINs a las tablas relacionadas.
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
    """
    Endpoint de API para consumo vía AJAX.
    Calcula dinámicamente el monto total a liquidar combinando la bonificación
    base del premio y el rendimiento alcanzado en el detalle del KPI.
    
    Fórmula:
        Monto Liquidado = Premio.Monto + KpiDetalle.Monto_Total
        
    Argumentos:
        request: Objeto HttpRequest.
        idPremio (int/str): Identificador del premio seleccionado.
        id_KPI (int/str): Identificador de la cabecera de KPI seleccionada.
        
    Retorna:
        JsonResponse con los estados 'success', 'monto_liquidado' o mensaje de 'error'.
    """

    try:
        # =====================================================
        # 1. BÚSQUEDA Y VALIDACIÓN DE MODELOS BASE
        # =====================================================
        # Obtiene la instancia del Premio mediante su ID; lanza error HTTP 404 si no existe
        premio = get_object_or_404(Premio, idPremio=idPremio)

        # Obtiene la cabecera del KPI asignado al empleado; lanza error HTTP 404 si no existe
        kpi = get_object_or_404(KpiCabecera, id_KPI=id_KPI)

        # =====================================================
        # 2. VALIDACIÓN DE COINCIDENCIA DE CATEGORÍA
        # =====================================================
        # Busca el detalle del KPI que coincida tanto con el KPI general 
        # como con la categoría específica requerida por el premio asignado
        detalle_kpi = KpiDetalle.objects.filter(
            id_KPI=kpi,
            id_KPI_Categoria=premio.id_KPI_Categoria
        ).first()

        # Si no hay registro de detalle para esa categoría, retorna respuesta JSON de error no bloqueante
        if detalle_kpi is None:
            return JsonResponse({
                'success': False,
                'error': (
                    'No existe un detalle de KPI para la categoría '
                    'asociada al premio seleccionado.'
                )
            })

        # =====================================================
        # 3. CÁLCULO Y SUCESO
        # =====================================================
        # Sumatoria del valor estático del premio + la puntuación/monto dinámico del detalle KPI
        monto_liquidado = premio.Monto + detalle_kpi.Monto_Total

        # Retorno de éxito estructurado para la previsualización en la plantilla del cliente
        return JsonResponse({
            'success': True,
            'monto_liquidado': float(monto_liquidado)  # Casting a float para asegurar la serialización JSON
        })

    # =========================================================
    # 4. MANEJO DE EXCEPCIONES INESPERADAS
    # =========================================================
    except Exception as e:
        # Captura cualquier falla imprevista (ej. tipos de datos incompatibles) y la expone al script AJAX
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# =========================================================================
# VISTA: Dashboard / Historial de KPIs
# =========================================================================
@requiere_permiso("kpi", "ver")  # Garantiza que el usuario tenga permisos de lectura en el módulo 'kpi'
def historial_kpi_view(request):
    """
    Consolida la información general del módulo de KPIs: historial detallado, premios asignados,
    métricas agrupadas (monto acumulado, promedio de alcance), ranking de colaboradores y resumen por categoría.
    
    Flujo de ejecución:
    1. Captura los parámetros de filtrado desde la URL (`GET`).
    2. Carga catálogos requeridos para los filtros desplegables.
    3. Construye y filtra la consulta de detalles (`KpiDetalle`) aplicando relaciones con `select_related`.
    4. Procesa agregaciones globales (`Sum`, `Avg`, `count`) para tarjetas informativas.
    5. Consulta y filtra el historial de premios asignados (`PremioAsignado`).
    6. Genera agrupaciones relacionales mediante `values()` y `annotate()` para ranking y resumen financiero.
    7. Renderiza el dashboard en la plantilla `kpi.html`.
    """

    # ── 1. Captura de filtros desde parámetros GET ─────────────────────────
    empleado_filtro_id = request.GET.get('empleado_filtro', '')
    mes_filtro         = request.GET.get('mes_filtro', '')
    anio_filtro        = request.GET.get('anio_filtro', '')

    # ── 2. Catálogos base para los selectores de la plantilla ────────────────
    # Carga empleados activos optimizando el JOIN con la tabla Persona
    empleados  = Empleado.objects.filter(Activo=True).select_related('idPersona')
    categorias = KpiCategoria.objects.all()

    # ── 3. Consulta base del historial de detalles ───────────────────────────
    # Inclusión de múltiples JOINs previos (select_related) para evitar peticiones N+1 al recorrer el listado
    detalles = KpiDetalle.objects.select_related(
        'id_KPI',
        'id_KPI__idEmpleado',
        'id_KPI__idEmpleado__idPersona',
        'id_KPI__idEmpleado__idPuesto',
        'id_KPI_Categoria',
    ).all()

    # ── 4. Aplicación dinámica de filtros a los detalles de KPI ─────────────
    if empleado_filtro_id:
        detalles = detalles.filter(id_KPI__idEmpleado_id=empleado_filtro_id)

    if mes_filtro:
        detalles = detalles.filter(id_KPI__mes=mes_filtro)

    if anio_filtro:
        detalles = detalles.filter(id_KPI__anio=anio_filtro)

    # Ordenamiento cronológico descendente (Año más reciente -> Mes más reciente)
    detalles = detalles.order_by('-id_KPI__anio', '-id_KPI__mes')

    # ── 5. Cálculo de métricas y estadísticas resumidas ──────────────────────
    total_kpis = detalles.count()
    
    # Sumatoria total pagada por concepto de bonos/detalles (retorna 0 si la consulta no devuelve registros)
    total_bonos = detalles.aggregate(t=Sum('Monto_Total'))['t'] or 0
    
    # Promedio global de porcentaje de alcance en los KPIs filtrados
    pct_promedio = detalles.aggregate(p=Avg('pct_Alcanzado'))['p'] or 0

    # ── 6. Consulta y filtrado de premios asignados ─────────────────────────
    premios_qs = PremioAsignado.objects.select_related(
        'idPremio',
        'id_KPI',
        'id_KPI__idEmpleado',
        'id_KPI__idEmpleado__idPersona',
        'idPremio__id_KPI_Categoria',
    ).all()

    # Replicación de la misma lógica de filtrado sobre el QuerySet de premios asignados
    if empleado_filtro_id:
        premios_qs = premios_qs.filter(id_KPI__idEmpleado_id=empleado_filtro_id)
    if mes_filtro:
        premios_qs = premios_qs.filter(id_KPI__mes=mes_filtro)
    if anio_filtro:
        premios_qs = premios_qs.filter(id_KPI__anio=anio_filtro)

    total_premios = premios_qs.count()

    # ── 7. Top 5 colaboradores con mejor rendimiento promedio ────────────────
    # Agrupa por colaborador y calcula el promedio del porcentaje alcanzado de sus KPIs
    top_colaboradores = (
        KpiDetalle.objects
        .values(
            'id_KPI__idEmpleado__idPersona__Nombre_Completo',
            'id_KPI__idEmpleado__idPuesto__Nombre',
            'id_KPI__idEmpleado__idPersona__Foto',
        )
        .annotate(pct_prom=Avg('pct_Alcanzado'))
        .order_by('-pct_prom')[:5]  # Limita el resultado a los mejores 5
    )

    # ── 8. Resumen financiero agrupado por categoría de KPI ───────────────────
    # Consolida el total invertido o pagado acumulado por cada tipo de categoría/indicador
    resumen_financiero = (
        KpiDetalle.objects
        .values('id_KPI_Categoria__tipo_categoria')
        .annotate(total=Sum('Monto_Total'))
        .order_by('-total')
    )

    # ── 9. Construcción del contexto y renderizado de respuesta ──────────────
    context = {
        'empleados': empleados,
        'categorias': categorias,

        # Mantenimiento de los filtros aplicados para la plantilla HTML
        'empleado_filtro_id': empleado_filtro_id,
        'mes_filtro': mes_filtro,
        'anio_filtro': anio_filtro,

        # Colecciones de registros principales
        'detalles': detalles,
        'premios_qs': premios_qs,

        # Indicadores numéricos (KPIs del dashboard)
        'total_kpis': total_kpis,
        'total_bonos': total_bonos,
        'pct_promedio': round(pct_promedio, 2),  # Redondeo de la métrica a 2 decimales
        'total_premios': total_premios,

        # Agregaciones para gráficos y tablas de resumen
        'top_colaboradores': top_colaboradores,
        'resumen_financiero': resumen_financiero,

        # Lista de mapeo para selector de meses en la interfaz
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
@requiere_permiso("onboarding", "ver")  # Exige al menos permisos de lectura/ver en el módulo 'onboarding'
def registrar_onboarding(request, pk=None):
    """
    Gestiona la creación, edición y visualización de la cabecera del proceso de Onboarding
    para un colaborador, además de cargar el listado de actividades asociadas.
    
    Flujo de ejecución:
    1. Evalúa el parámetro opcional `pk`:
       - Si está presente, recupera la instancia existente de `Onboarding` y habilita el 'paso dos'.
       - Si es `None`, se prepara para crear un registro nuevo.
    2. Si la petición es POST:
       a. Determina dinámicamente la acción ('crear' o 'editar') para validar permisos con `bloquear_si_no_puede`.
       b. Instancia `OnboardingForm` con los datos recibidos (request.POST) e instancia actual.
       c. Si el formulario es válido, guarda el registro y redirige a la vista de gestión (`gestionar_onboarding`).
    3. Si la petición es GET:
       a. Instancia el formulario `OnboardingForm` (vacío o cargado con la instancia existente).
    4. Consulta el catálogo general de actividades de onboarding con JOINs optimizados via `select_related`.
    5. Renderiza la interfaz `onboarding.html` con ambos formularios y el contexto necesario.
    """

    # Inicialización de variables para el control de la interfaz
    onboarding = None
    paso_dos_habilitado = False

    # ── 1. Carga de instancia existente (Modo Edición / Detalle) ───────────
    if pk:
        # Recupera el proceso de Onboarding por ID; si no existe, lanza un HTTP 404
        onboarding = get_object_or_404(
            Onboarding,
            pk=pk
        )

        # Habilita en el frontend el formulario secundario / paso 2 (asignación de actividades)
        paso_dos_habilitado = True

    # ── 2. Procesamiento del Formulario (POST) ─────────────────────────────
    if request.method == "POST":

        # Determina la acción para evaluar permisos según la existencia de la instancia
        accion = "editar" if onboarding else "crear"

        # Verificación explícita de seguridad con base en la acción identificada
        bloqueo = bloquear_si_no_puede(
            request,
            "onboarding",
            accion
        )

        if bloqueo:
            return bloqueo  # Corta el flujo si el usuario carece de permisos de creación/edición

        # Instancia el formulario vinculando la data POST y el objeto (para crear o actualizar)
        form = OnboardingForm(
            request.POST,
            instance=onboarding
        )

        # Validaciones de reglas de modelo y campos requeridos
        if form.is_valid():

            # Inserción o actualización en la base de datos
            nuevo = form.save()

            messages.success(
                request,
                f"Proceso de Onboarding #{nuevo.id_Onboarding} creado correctamente."
            )

            # Redirección mediante el patrón Post/Redirect/Get hacia la gestión detallada
            return redirect(
                "gestionar_onboarding",
                pk=nuevo.id_Onboarding
            )

        else:

            # Notificación de error si falla la validación
            messages.error(
                request,
                "Revise los datos del formulario."
            )

    # ── 3. Solicitud inicial (GET) ──────────────────────────────────────────
    else:

        # Instancia el formulario limpio o precargado con los datos del Onboarding existente
        form = OnboardingForm(
            instance=onboarding
        )

    # =====================================================
    # CARGAR ACTIVIDADES REGISTRADAS
    # =====================================================
    # Optimización ORM con select_related para evitar peticiones N+1 al listar las actividades,
    # ordenadas de forma descendente por el ID del proceso de Onboarding.
    actividades = OnboardingActividad.objects.select_related(
        "idActividad",
        "id_Estatus_Vacante",
        "id_Onboarding"
    ).all().order_by(
        "-id_Onboarding__id_Onboarding"
    )

    # ── 4. Construcción del Contexto y Renderizado ─────────────────────────
    context = {
        "form": form,                                     # Formulario de cabecera (OnboardingForm)
        "form_detalle": OnboardingActividadForm(),       # Formulario secundario para agregar actividades
        "onboarding": onboarding,                         # Instancia del onboarding (o None)
        "paso_dos_habilitado": paso_dos_habilitado,       # Flag para activar la segunda etapa en el HTML
        "actividades": actividades,                       # Listado general de actividades
    }

    return render(
        request,
        "onboarding.html",
        context
    )



# =========================================================
# GUARDAR DETALLE DE ACTIVIDAD DEL ONBOARDING
# =========================================================
@requiere_permiso("onboarding", "editar")  # Restringe la acción a usuarios con permiso de modificación en 'onboarding'
def guardar_detalle_onboarding(request, pk):
    """
    Asigna y guarda una nueva actividad específica dentro del proceso de Onboarding de un colaborador.
    
    Argumentos:
        request: Objeto HttpRequest de Django.
        pk (int/str): Identificador primario de la cabecera de Onboarding existente.

    Flujo de ejecución:
    1. Obtiene la cabecera del proceso (`Onboarding`) o responde con HTTP 404 si no existe.
    2. Procesa la solicitud si es de tipo POST.
    3. Instancia el formulario `OnboardingActividadForm` con los datos enviados.
    4. Si el formulario es válido:
       a. Crea el objeto en memoria sin guardar en BD (`commit=False`).
       b. Asigna la relación de clave foránea con la cabecera (`id_Onboarding`).
       c. Guarda la actividad en la base de datos de manera definitiva.
    5. Maneja posibles excepciones de base de datos (`IntegrityError`) o errores imprevistos.
    6. En caso de fallos de validación, itera y notifica los errores por cada campo.
    7. Redirige siempre a la vista principal de gestión del Onboarding actual.
    """

    # 1. Obtención y validación de la cabecera padre
    onboarding = get_object_or_404(Onboarding, pk=pk)

    # 2. Procesamiento del envío del formulario (POST)
    if request.method == "POST":
        # Instancia el formulario vinculando los datos enviados por el usuario
        form = OnboardingActividadForm(request.POST)

        # Validaciones de tipos de datos y reglas del formulario
        if form.is_valid():
            try:
                # Instancia el objeto OnboardingActividad en memoria reteniendo el guardado en la BD
                detalle = form.save(commit=False)
                
                # Asocia manualmente la clave foránea del Onboarding recuperado previamente
                detalle.id_Onboarding = onboarding
                
                # Guarda definitivamente el registro en la base de datos
                detalle.save()

                # Notificación de éxito al usuario
                messages.success(request, "Actividad registrada correctamente.")

            except IntegrityError as e:
                # Captura violaciones de restricciones en la BD (ej. valores nulos no permitidos, claves duplicadas)
                messages.error(
                    request, 
                    f"Error de base de datos al registrar la actividad: {e}"
                )
            except Exception as e:
                # Captura cualquier otra falla inesperada durante el proceso de guardado
                messages.error(
                    request, 
                    f"Ocurrió un error inesperado al guardar la actividad: {e}"
                )
        else:
            # Iteración sobre los errores de validación del formulario para notificar al usuario campo por campo
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")

    # 3. Redirección asegurada a la pantalla de gestión principal del Onboarding (Patrón PRG)
    return redirect("gestionar_onboarding", pk=onboarding.pk)



def elec_Offboarding_view(request):
    return render(request, 'elec_Offboarding.html')


# =========================================================
# GUARDAR CABECERA DEL OFFBOARDING
# Proceso de salida de un empleado
# =========================================================
@requiere_permiso("offboarding", "ver")  # Restringe la vista a usuarios que cuenten con permiso de lectura en 'offboarding'
def registrar_offboarding(request, pk=None):
    """
    Gestiona la creación, edición y consulta histórica de la cabecera del proceso de desvinculación 
    (Offboarding) de un colaborador.
    
    Argumentos:
        request: Objeto HttpRequest de Django.
        pk (int/str, opcional): Identificador primario del proceso de Offboarding a editar/visualizar.

    Flujo de ejecución:
    1. Evalúa el parámetro opcional `pk`:
       - Si está presente, recupera el objeto `Offboarding` y habilita el 'paso dos' de la interfaz.
       - Si es `None`, se prepara para un nuevo registro.
    2. Si la petición es POST:
       a. Determina dinámicamente la acción ('crear' o 'editar') para validar permisos con `bloquear_si_no_puede`.
       b. Instancia `OffboardingForm` con los datos enviados (request.POST) e instancia actual.
       c. Si el formulario es válido, guarda el registro y redirige a la vista de gestión (`gestionar_offboarding`).
    3. Si la petición es GET:
       a. Instancia `OffboardingForm` (vacío o cargado con la información previa del registro).
    4. Consulta la lista completa de procesos de Offboarding optimizando los JOINs con `select_related`.
    5. Renderiza la plantilla `registrar_off.html` con el formulario y el historial de salidas.
    """

    # Inicialización de variables para el flujo de la vista
    offboarding = None
    paso_dos_habilitado = False

    # ── 1. Carga de registro existente (Modo Edición / Detalle) ────────────
    if pk:
        # Busca el proceso de Offboarding por clave primaria; si no existe, genera una respuesta HTTP 404
        offboarding = get_object_or_404(
            Offboarding,
            pk=pk
        )

        # Activa la segunda etapa/paso en la plantilla frontend (ej. asignación de tareas de desvinculación)
        paso_dos_habilitado = True

    # ── 2. Procesamiento de la Petición POST (Crear / Editar) ─────────────
    if request.method == "POST":

        # Evalúa la acción a ejecutar según si se trata de un registro previo o una nueva entrada
        accion = "editar" if offboarding else "crear"

        # Validación explícita de seguridad para verificar permisos específicos del usuario
        bloqueo = bloquear_si_no_puede(
            request,
            "offboarding",
            accion
        )

        if bloqueo:
            return bloqueo  # Detiene el flujo si el usuario no tiene los permisos requeridos

        # Asocia los datos recibidos con la instancia del formulario
        form = OffboardingForm(
            request.POST,
            instance=offboarding
        )

        # Validación del formulario conforme a las reglas del Modelo
        if form.is_valid():

            # Guarda o actualiza el registro en la base de datos
            nuevo = form.save()

            messages.success(
                request,
                f"Proceso de Offboarding #{nuevo.id_Offboarding} creado correctamente."
            )

            # Redirección aplicando el patrón Post/Redirect/Get hacia la gestión detallada
            return redirect(
                "gestionar_offboarding",
                pk=nuevo.id_Offboarding
            )

        else:

            # Notificación de error si falla la validación del formulario
            messages.error(
                request,
                "Revise los datos del formulario."
            )

    # ── 3. Petición Inicial GET ───────────────────────────────────────────
    else:

        # Genera el formulario limpio para creación o precargado para edición
        form = OffboardingForm(
            instance=offboarding
        )

    # ── 4. Construcción del Contexto y Renderizado de la Plantilla ─────────
    # Consulta el listado de salidas históricas utilizando select_related para traer 
    # en una sola consulta SQL los datos del empleado, su información personal y la causa de salida.
    context = {
        "form": form,                                    # Formulario principal del proceso
        "offboarding": offboarding,                      # Instancia del proceso cargado (o None)
        "paso_dos_habilitado": paso_dos_habilitado,      # Flag de control para habilitar el paso 2
        "offboardings": Offboarding.objects.select_related(
            "idEmpleado__idPersona",
            "idCausa"
        ).order_by("-Fecha_Salida")                       # Orden cronológico descendente por fecha de salida
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
@requiere_permiso("offboarding", "ver")  # Restringe el acceso a usuarios con permiso de lectura en 'offboarding'
def guardar_checklist_offboarding(request):
    """
    Gestiona la creación, actualización y sincronización de tareas/actividades (checklist) 
    asociadas a un proceso de desvinculación (Offboarding).

    Argumentos:
        request: Objeto HttpRequest de Django.

    Flujo de ejecución:
    1. Si es POST:
       a. Extrae los parámetros enviados desde el formulario (IDs, fechas, lista de actividades).
       b. Valida que los campos obligatorios estén presentes (Offboarding, Estado, Actividades).
       c. Determina la acción ('crear' o 'editar') y valida permisos con `bloquear_si_no_puede`.
       d. Calcula dinámicamente el porcentaje de avance (`pct_listo`) con base en el catálogo total.
       e. Inicia una transacción atómica (`transaction.atomic()`):
          - Crea o actualiza la cabecera `OffboardingChecklist`.
          - Elimina los detalles previos en `OffboardingChecklistDetalle`.
          - Reinserta los detalles seleccionados.
       f. Captura excepciones de integridad o fallos inesperados.
    2. Construye el contexto necesario para el renderizado (procesos de Offboarding, catálogo, estatus).
    3. Renderiza la plantilla `checklist_off.html`.
    """

    if request.method == "POST":

        try:

            # =====================================================
            # 1. EXTRACCIÓN DE DATOS RECIBIDOS DEL FORMULARIO
            # =====================================================
            id_offboarding = request.POST.get("id_Offboarding")
            id_estatus = request.POST.get("id_Estatus_Vacante")
            fecha_comp = request.POST.get("Fecha_Comp")
            observacion = request.POST.get("Observacion")
            # Obtiene la lista de IDs del catálogo seleccionados en los checkboxes
            actividades = request.POST.getlist("actividades[]")

            # =====================================================
            # 2. VALIDACIONES DE CAMPOS OBLIGATORIOS
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
                # 3. OBTENCIÓN DE ENTIDADES ASOCIADAS
                # =================================================
                # Valida que el proceso de Offboarding exista en la BD
                offboarding = get_object_or_404(
                    Offboarding,
                    id_Offboarding=id_offboarding
                )

                # Valida que el estado/estatus exista en la BD
                estado = get_object_or_404(
                    Estatus,
                    id_Estatus_Vacante=id_estatus
                )

                # =================================================
                # 4. DETERMINACIÓN DE ACCIÓN Y VERIFICACIÓN DE PERMISOS
                # =================================================
                try:
                    # Intenta recuperar un checklist previo para saber si es una edición
                    OffboardingChecklist.objects.get(
                        id_Offboarding=offboarding
                    )
                    accion = "editar"

                except OffboardingChecklist.DoesNotExist:
                    # Si no existe, la acción será una creación
                    accion = "crear"

                # Verificación explícita de seguridad según la acción determinada
                bloqueo = bloquear_si_no_puede(
                    request,
                    "offboarding",
                    accion
                )

                if bloqueo:
                    return bloqueo  # Detiene el flujo si carece de permisos

                # =================================================
                # 5. CÁLCULO DEL PORCENTAJE DE AVANCE
                # =================================================
                total_catalogo = OffboardingCatalogo.objects.count()
                total_seleccionadas = len(actividades)

                if total_catalogo > 0:
                    # Registra el avance proporcional según el total de items en el catálogo global
                    pct_listo = round(
                        (total_seleccionadas / total_catalogo) * 100,
                        2
                    )
                else:
                    pct_listo = Decimal("0.00")

                # =================================================
                # 6. OPERACIONES DENTRO DE TRANSACCIÓN ATÓMICA
                # =================================================
                # Garantiza que todas las operaciones en BD (cabecera y detalles) se ejecuten o reviertan juntas
                with transaction.atomic():

                    # Intenta recuperar la cabecera existente
                    try:
                        checklist = OffboardingChecklist.objects.get(
                            id_Offboarding=offboarding
                        )
                        creado = False

                    # Si no existe, registra la nueva cabecera
                    except OffboardingChecklist.DoesNotExist:
                        checklist = OffboardingChecklist.objects.create(
                            Fecha_Asignacion=date.today(),
                            Fecha_Comp=fecha_comp if fecha_comp else None,
                            Observacion=observacion,
                            pct_listo=pct_listo,
                            id_Offboarding=offboarding,
                            id_Estatus_Vacante=estado
                        )
                        creado = True

                    # Si ya existía la cabecera, actualiza sus valores
                    if not creado:
                        checklist.Fecha_Comp = fecha_comp if fecha_comp else None
                        checklist.Observacion = observacion
                        checklist.pct_listo = pct_listo
                        checklist.id_Estatus_Vacante = estado
                        checklist.save()

                    # Estrategia de sincronización de detalles: limpia registros anteriores
                    OffboardingChecklistDetalle.objects.filter(
                        id_Check=checklist
                    ).delete()

                    registros_creados = 0

                    # Reinserta las actividades que fueron marcadas en la interfaz
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

                # Feedback al usuario según el resultado de la transacción
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
            # Captura de errores de restricciones en la base de datos
            print("ERROR DE INTEGRIDAD:", e)
            messages.error(
                request,
                f"Error de integridad en la base de datos: {e}"
            )

        except Exception as e:
            # Captura de errores imprevistos
            print("ERROR:", e)
            messages.error(
                request,
                f"Error al guardar el checklist: {e}"
            )

    # =========================================================
    # 7. CONSTRUCCIÓN DEL CONTEXTO PARA LA VISTA (GET / POST)
    # =========================================================

    # Consulta optimizada de procesos de Offboarding con JOINs a Empleado, Persona y Causa
    offboardings = Offboarding.objects.select_related(
        "idEmpleado",
        "idEmpleado__idPersona",
        "idCausa"
    ).order_by("-Fecha_Salida")

    # Mapea dinámicamente el objeto Checklist correspondiente a cada proceso para usar en plantilla
    for proceso in offboardings:
        try:
            proceso.checklist_obj = OffboardingChecklist.objects.get(
                id_Offboarding=proceso.id_Offboarding
            )
        except OffboardingChecklist.DoesNotExist:
            proceso.checklist_obj = None

    # Agrupa los catálogos y referencias necesarias para construir los controles de la plantilla
    context = {
        "offboardings": offboardings,
        "catalogo": OffboardingCatalogo.objects.order_by(
            "Num_Etapa",
            "idCatalogo"
        ),
        "checklists": OffboardingChecklist.objects.select_related(
            "id_Offboarding",
            "id_Estatus_Vacante"
        ).order_by("-Fecha_Asignacion"),
        "estados": Estatus.objects.order_by("id_Estatus_Vacante")
    }

    # Renderizado final de la vista
    return render(
        request,
        "checklist_off.html",
        context
    )


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
@requiere_permiso("usuarios_sistema", "crear")  # Restringe la acción a usuarios con permiso de creación en 'usuarios_sistema'
def guardar_usuario_sistema(request):
    """
    Gestiona el registro e inserción de nuevas cuentas de acceso al sistema (UsuarioSistema),
    vinculándolas con un empleado activo y un rol específico, además de renderizar la gestión general de usuarios.

    Argumentos:
        request: Objeto HttpRequest de Django.

    Flujo de ejecución:
    1. Si es POST:
       a. Extrae y sanitiza (`strip()`) los datos recibidos del formulario (correo, contraseña, rol, empleado, activo).
       b. Ejecuta un flujo de validaciones secuenciales:
          - Campos obligatorios (correo, contraseña, rol, empleado, estado).
          - Unicidad de correo electrónico en la base de datos.
          - Relación 1:1 con Empleado (evita duplicar usuario a un mismo empleado).
       c. Si supera las validaciones, obtiene las instancias referenciadas (`Roles`, `Empleado`).
       d. Hashea la contraseña con `make_password` y registra la entidad `UsuarioSistema`.
       e. Si todo se procesa correctamente, redirige mediante PRG para evitar reenvíos de formulario.
       f. Captura posibles violaciones de unicidad en BD (`IntegrityError`) o excepciones generales.
    2. Si es GET (o falla la petición/redirección):
       - Construye el contexto consultando catálogos de empleados activos, roles y lista global de usuarios
         aplicando optimizaciones ORM (`select_related`).
    3. Renderiza la plantilla `usuarios.html`.
    """

    if request.method == "POST":

        # ── 1. Limpieza y extracción inicial de inputs ──────────────────────
        correo = request.POST.get("Correo", "").strip()
        contrasenia = request.POST.get("Contrasenia", "").strip()
        id_rol = request.POST.get("idRol")
        id_empleado = request.POST.get("idEmpleado_Admin")
        activo_raw = request.POST.get("Activo")

        # ── 2. Validaciones básicas y reglas de negocio ─────────────────────
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

        # Validación de unicidad: No se permite registrar un correo que ya exista
        elif UsuarioSistema.objects.filter(Correo=correo).exists():
            messages.error(request, "Ya existe un usuario registrado con ese correo.")

        # Validación de relación 1 a 1: Garantiza que un empleado solo posea una cuenta de acceso
        elif UsuarioSistema.objects.filter(idEmpleado_Admin=id_empleado).exists():
            messages.error(request, "El empleado seleccionado ya tiene un usuario asignado.")

        else:
            try:
                # ── 3. Recuperación de modelos relacionados ───────────────────
                # Búsqueda directa por clave primaria para el INSERT (sin joins innecesarios)
                rol = get_object_or_404(Roles, pk=id_rol)
                empleado = get_object_or_404(Empleado, pk=id_empleado)

                # ── 4. Creación e inserción del nuevo usuario ────────────────
                UsuarioSistema.objects.create(
                    Correo=correo,
                    Contrasenia=make_password(contrasenia),  # Encriptación segura de la contraseña
                    idRol=rol,
                    Activo=(activo_raw == "1"),             # Conversión a valor booleano
                    idEmpleado_Admin=empleado
                )

                messages.success(request, "Usuario registrado correctamente.")
                
                # Redirección para aplicar el patrón Post/Redirect/Get (PRG)
                return redirect("guardar_usuario_sistema")

            except IntegrityError as e:
                # Captura violaciones de claves únicas directamente notificadas por la BD
                messages.error(
                    request, 
                    "Error de integridad: El correo o el empleado ya se encuentran vinculados a otro usuario."
                )
            except Exception as e:
                # Captura de fallas imprevistas durante la inserción
                messages.error(request, f"Ocurrió un error al guardar el usuario: {e}")

    # ── 5. Carga de datos para el Template (GET o fallback tras POST) ────────
    # Se obtienen los catálogos requeridos para renderizar el formulario y el listado general
    context = {
        # Lista de empleados activos ordenados alfabéticamente por nombre
        "empleados": Empleado.objects.select_related(
            "idPersona", 
            "idPuesto"
        ).filter(
            Activo=True
        ).order_by(
            "idPersona__Nombre_Completo"
        ),

        # Catálogo de roles disponibles
        "roles": Roles.objects.order_by("TipoRol"),

        # Listado global de usuarios optimizado con select_related para traer Persona y Puesto en un solo JOIN
        "usuarios": UsuarioSistema.objects.select_related(
            "idRol",
            "idEmpleado_Admin",
            "idEmpleado_Admin__idPersona",
            "idEmpleado_Admin__idPuesto"
        ).order_by("Correo")
    }

    # ── 6. Renderizado de la respuesta ──────────────────────────────────────
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



# =========================================================
# GUARDAR USUARIO DEL SISTEMA
# =========================================================
@requiere_permiso("usuarios_sistema", "crear")  # Restringe la acción a usuarios con permiso de creación en 'usuarios_sistema'
def guardar_usuario_sistema(request):
    """
    Gestiona el registro e inserción de nuevas cuentas de acceso al sistema (UsuarioSistema),
    vinculándolas con un empleado activo y un rol específico, además de renderizar la gestión general de usuarios.

    Argumentos:
        request: Objeto HttpRequest de Django.

    Flujo de ejecución:
    1. Si es POST:
       a. Extrae y sanitiza (`strip()`) los datos recibidos del formulario (correo, contraseña, rol, empleado, activo).
       b. Ejecuta un flujo de validaciones secuenciales:
          - Campos obligatorios (correo, contraseña, rol, empleado, estado).
          - Unicidad de correo electrónico en la base de datos.
          - Relación 1:1 con Empleado (evita duplicar usuario a un mismo empleado).
       c. Si supera las validaciones, obtiene las instancias referenciadas (`Roles`, `Empleado`).
       d. Hashea la contraseña con `make_password` y registra la entidad `UsuarioSistema`.
       e. Si todo se procesa correctamente, redirige mediante PRG para evitar reenvíos de formulario.
       f. Captura posibles violaciones de unicidad en BD (`IntegrityError`) o excepciones generales.
    2. Si es GET (o falla la petición/redirección):
       - Construye el contexto consultando catálogos de empleados activos, roles y lista global de usuarios
         aplicando optimizaciones ORM (`select_related`).
    3. Renderiza la plantilla `usuarios.html`.
    """

    if request.method == "POST":

        # ── 1. Limpieza y extracción inicial de inputs ──────────────────────
        correo = request.POST.get("Correo", "").strip()
        contrasenia = request.POST.get("Contrasenia", "").strip()
        id_rol = request.POST.get("idRol")
        id_empleado = request.POST.get("idEmpleado_Admin")
        activo_raw = request.POST.get("Activo")

        # ── 2. Validaciones básicas y reglas de negocio ─────────────────────
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

        # Validación de unicidad: No se permite registrar un correo que ya exista
        elif UsuarioSistema.objects.filter(Correo=correo).exists():
            messages.error(request, "Ya existe un usuario registrado con ese correo.")

        # Validación de relación 1 a 1: Garantiza que un empleado solo posea una cuenta de acceso
        elif UsuarioSistema.objects.filter(idEmpleado_Admin=id_empleado).exists():
            messages.error(request, "El empleado seleccionado ya tiene un usuario asignado.")

        else:
            try:
                # ── 3. Recuperación de modelos relacionados ───────────────────
                # Búsqueda directa por clave primaria para el INSERT (sin joins innecesarios)
                rol = get_object_or_404(Roles, pk=id_rol)
                empleado = get_object_or_404(Empleado, pk=id_empleado)

                # ── 4. Creación e inserción del nuevo usuario ────────────────
                UsuarioSistema.objects.create(
                    Correo=correo,
                    Contrasenia=make_password(contrasenia),  # Encriptación segura de la contraseña
                    idRol=rol,
                    Activo=(activo_raw == "1"),             # Conversión a valor booleano
                    idEmpleado_Admin=empleado
                )

                messages.success(request, "Usuario registrado correctamente.")
                
                # Redirección para aplicar el patrón Post/Redirect/Get (PRG)
                return redirect("guardar_usuario_sistema")

            except IntegrityError as e:
                # Captura violaciones de claves únicas directamente notificadas por la BD
                messages.error(
                    request, 
                    "Error de integridad: El correo o el empleado ya se encuentran vinculados a otro usuario."
                )
            except Exception as e:
                # Captura de fallas imprevistas durante la inserción
                messages.error(request, f"Ocurrió un error al guardar el usuario: {e}")

    # ── 5. Carga de datos para el Template (GET o fallback tras POST) ────────
    # Se obtienen los catálogos requeridos para renderizar el formulario y el listado general
    context = {
        # Lista de empleados activos ordenados alfabéticamente por nombre
        "empleados": Empleado.objects.select_related(
            "idPersona", 
            "idPuesto"
        ).filter(
            Activo=True
        ).order_by(
            "idPersona__Nombre_Completo"
        ),

        # Catálogo de roles disponibles
        "roles": Roles.objects.order_by("TipoRol"),

        # Listado global de usuarios optimizado con select_related para traer Persona y Puesto en un solo JOIN
        "usuarios": UsuarioSistema.objects.select_related(
            "idRol",
            "idEmpleado_Admin",
            "idEmpleado_Admin__idPersona",
            "idEmpleado_Admin__idPuesto"
        ).order_by("Correo")
    }

    # ── 6. Renderizado de la respuesta ──────────────────────────────────────
    return render(request, "usuarios.html", context)



# =========================================================
# VISTA: MÓDULO DE REPORTES DE ACCIONES DE PERSONAL
# =========================================================
@requiere_permiso("acciones_personal", "ver")  # Restringe el acceso a usuarios con permiso de lectura en 'acciones_personal'
def modulo_reportes(request):
    """
    Consolida, agrupa y serializa la información histórica de las acciones de personal por colaborador, 
    así como datos de rotación y el listado de empleados activos para la generación de reportes e informes.

    Argumentos:
        request: Objeto HttpRequest de Django.

    Flujo de ejecución:
    1. Consulta el historial de `AccionTipo` optimizando relaciones (`select_related`) para evitar consultas N+1.
    2. Agrupa dinámicamente las acciones registradas por colaborador en un diccionario (`empleados_dict`), 
       extrayendo datos personales, de puesto, departamento y el detalle particular de cada movimiento.
    3. Serializa la estructura agrupada a formato JSON (`DjangoJSONEncoder`) para su fácil manipulación en el cliente/JS.
    4. Consulta los registros históricos de rotación de personal (`RotacionPersonal`).
    5. Carga el catálogo general de empleados activos con sus correspondientes datos de `Persona` y `Puesto`.
    6. Renderiza la plantilla `reportes.html` enviando las colecciones de datos procesadas.
    """

    # ── 1. Consulta optimizada del historial de acciones de personal ───────
    # Incluye en un solo JOIN profundo las relaciones con Empleado, Persona, Puesto, Departamento, Detalle y Premios
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

    # Diccionario temporal para consolidar la información agrupada por ID de empleado
    empleados_dict = {}

    # ── 2. Procesamiento y agrupación de datos por colaborador ────────────
    for item in acciones:
        # Extrae la instancia del empleado vinculada a la acción de personal
        emp = item.idAccion.idEmpleado if item.idAccion else None
        
        # Ignora registros huérfanos o que no tengan entidad de Persona asociada
        if not emp or not emp.idPersona:
            continue

        emp_id = str(emp.pk)

        # Si el empleado aún no está registrado en el diccionario, inicializa su estructura base
        if emp_id not in empleados_dict:
            persona = emp.idPersona
            puesto = emp.idPuesto
            
            # Obtiene el departamento de forma segura previniendo errores de atributos inexistentes
            departamento = puesto.idDepartamento if puesto and hasattr(puesto, 'idDepartamento') else None

            # Extracción defensiva de propiedades para evitar fallos por valores nulos
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
                'acciones': []  # Lista que contendrá el detalle de cada acción del colaborador
            }

        # Extrae el detalle específico de la acción (prioriza el propio registro sobre la categoría)
        detalle_especifico = item.Detalle or (item.id_Detalle_Accion.Detalle if item.id_Detalle_Accion else '')

        # Agrega la acción actual a la lista de acciones del colaborador correspondiente
        empleados_dict[emp_id]['acciones'].append({
            'tipo': item.id_Detalle_Accion.Accion if item.id_Detalle_Accion else 'Otro',
            'detalle': detalle_especifico,
            'fecha': item.idAccion.Fecha.strftime('%d/%m/%Y') if item.idAccion and item.idAccion.Fecha else '',
            'anio': item.idAccion.Fecha.year if item.idAccion and item.idAccion.Fecha else None,
            'mes': item.idAccion.Fecha.month if item.idAccion and item.idAccion.Fecha else None,
        })

    # ── 3. Serialización a JSON y consultas complementarias ──────────────
    # Convierte la estructura agrupada de colaboradores a JSON para su uso en componentes JS/DataTables
    empleados_json = json.dumps(list(empleados_dict.values()), cls=DjangoJSONEncoder)
    
    # Consulta el historial de rotaciones ordenado cronológicamente (Año -> Mes descendente)
    rotaciones = RotacionPersonal.objects.order_by('-Anio', '-Mes')

    # Consulta optimizada para el listado general de empleados activos (para filtros o selectores)
    todos_los_empleados = Empleado.objects.select_related(
        'idPersona', 
        'idPuesto'
    ).filter(
        Activo=True
    ).order_by('idPersona__Nombre_Completo')

    # ── 4. Construcción del Contexto y Renderizado de la Respuesta ──────────
    context = {
        'acciones': acciones,                                  # QuerySet original de acciones de personal
        'empleados_lista': list(empleados_dict.values()),      # Lista estructurada en Python
        'todos_los_empleados': todos_los_empleados,            # Lista de empleados activos para filtros
        'empleados_data_json': empleados_json,                 # Data estructurada en JSON para JS
        'rotaciones': rotaciones,                              # QuerySet de rotación de personal
    }

    return render(request, 'reportes.html', context)



def configuraciones_view(request):
    return render(request, 'configuraciones.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('login_usuario')
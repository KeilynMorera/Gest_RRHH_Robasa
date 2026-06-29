from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from decimal import Decimal
from django.db.models import Max
from django.db.models import Sum
from datetime import date, datetime
from django.contrib import messages
from .forms import AccionPersonalForm
from django.db import transaction
from django.db import IntegrityError
from .forms import PremioForm
from django.utils import timezone
from .forms import PremioAsignadoForm
from django.db.models import Q # Asegúrate de tener esta importación al inicio de tu archivo views.py

#Importa todo lo que se encuentra en el archivo models.py
#Donde se encuentran los modelos de las tablas de la base de datos
from .models import *

# =========================================================
# Vista: Login
# =========================================================
def home(request):
    return render(request, 'login.html')

# =========================================================
# Vista: Inicio
# =========================================================
def inicio_view(request):
    return render(request, 'inicio.html')

# =========================================================
# Vista: Elección Complementos de la Empresa: Gerencia, Departamento y Puesto
# =========================================================

def comple_Empresa_view(request):
    return render(request, 'comple_Empresa.html')



# =========================================================
# Vista: Empresas — registro, modificación y listado
# NOTA: esta función reemplaza tanto 'registrar_empresa'
#       como 'empresas_view'. En urls.py debe quedar
#       una sola ruta apuntando aquí con name='empresas'.
# =========================================================
# =========================================================
# Vista: Empresas — registro, modificación y listado
# =========================================================
def registrar_empresa(request):

    # ─────────────────────────────────────────────
    # POST → Crear o Modificar empresa
    # ─────────────────────────────────────────────
    if request.method == 'POST':

        accion = request.POST.get('accion')
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
def eliminar_empresa(request, idEmpresa):

    empresa = get_object_or_404(
        Empresa,
        pk=idEmpresa
    )

    empresa.delete()

    return redirect('empresas')



# =========================================================
# Vista: Gerencias — registro, edición y listado
# =========================================================
def gerencias_view(request):
 
    if request.method == 'POST':
        gerencia_id  = request.POST.get('gerencia_id')  # vacío = nuevo registro
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
def eliminar_gerencia_view(request, pk):
    Gerencia.objects.filter(pk=pk).delete()
    return redirect('gerencias')



# =========================================================
# Vista: Departamentos — registro, edición y listado
# =========================================================
def departamentos_view(request):

    if request.method == 'POST':

        departamento_id = request.POST.get('departamento_id')
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
def eliminar_departamento_view(request, pk):

    Departamento.objects.filter(
        pk=pk
    ).delete()

    return redirect('departamentos')



# =========================================================
# Vista: Puestos — registro, edición y listado
# =========================================================
def puestos_view(request):

    if request.method == 'POST':

        puesto_id = request.POST.get('puesto_id')
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
def eliminar_puesto_view(request, pk):

    Puesto.objects.filter(
        pk=pk
    ).delete()

    return redirect('puestos')


# =========================================================
# Vista: Compensación de Puestos — registro, edición y listado
# =========================================================
def compensacion_puesto_view(request):

    if request.method == 'POST':

        compensacion_id = request.POST.get('compensacion_id')

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
def eliminar_compensacion_puesto_view(request, pk):
    Compensacion_Puesto.objects.filter(pk=pk).delete()
    return redirect('compensacion_puesto')   # ← mismo name que usás arriba



# =========================================================
# Vista: Elección Personas, Empleados o Pasantes
# =========================================================
def per_emp_view(request):
    return render(request, 'per_emp.html')



# =========================================================
# Vista: Personas — registro, modificación y listado
# NOTA: esta función reemplaza tanto 'registrar_persona'
#       como 'personas_view'. En urls.py debe quedar
#       una sola ruta apuntando aquí con name='personas'.
# =========================================================
def registrar_persona(request):

    # ── POST: crear o modificar ────────────────────────────
    if request.method == 'POST':
        accion     = request.POST.get('accion')      # 'crear' o 'modificar'
        persona_id = request.POST.get('persona_id')  # vacío si es nuevo

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


def editar_persona(request, id_persona):

    persona = get_object_or_404(
        Persona,
        pk=id_persona
    )

    if request.method == 'POST':

        persona.Nombre_Completo = request.POST.get('nombre_completo')
        persona.Cedula = request.POST.get('cedula')
        persona.Sexo = request.POST.get('sexo')
        persona.FechaNacimiento = request.POST.get('fecha_nacimiento')
        persona.Telefono = request.POST.get('telefono')
        persona.Celular = request.POST.get('celular')
        persona.Correo = request.POST.get('correo')
        persona.Direccion = request.POST.get('direccion')

        if request.FILES.get('foto'):
            persona.Foto = request.FILES['foto']

        persona.save()

        return redirect('personas')

    personas = Persona.objects.all()
    sexos = PersonaSexo.objects.all()
    
    return render(
        request, 'personas.html', {
            'persona_editar': persona,
            'personas': personas,'sexos': sexos
    }
)

# =========================================================
# Vista: Eliminar Persona
# =========================================================
def eliminar_persona(request, id_persona):
    persona = get_object_or_404(Persona, pk=id_persona)
    persona.delete()
    return redirect('personas')



# =========================================================
# Vista: Empleados — registro, modificación y listado
# =========================================================
def registrar_empleado(request):

    # ── POST: crear o modificar ────────────────────────────
    if request.method == 'POST':
        accion      = request.POST.get('accion')       # 'crear' o 'modificar'
        empleado_id = request.POST.get('empleado_id')  # vacío si es nuevo

        persona_id    = request.POST.get('persona')
        puesto_id     = request.POST.get('puesto')
        contrato_id   = request.POST.get('contrato')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        activo        = request.POST.get('activo')     # '1' o '0'

        persona_obj  = Persona.objects.get(pk=persona_id)
        puesto_obj   = Puesto.objects.get(pk=puesto_id)
        contrato_obj = Contrato.objects.get(pk=contrato_id)
        activo_bool  = activo == '1'

        if accion == 'crear' or not accion:
            Empleado.objects.create(
                idPersona     = persona_obj,
                idPuesto      = puesto_obj,
                idContrato    = contrato_obj,
                Fecha_Ingreso = fecha_ingreso,
                Activo        = activo_bool,
            )

        elif accion == 'modificar' and empleado_id:
            empleado = Empleado.objects.get(pk=empleado_id)
            empleado.idPersona     = persona_obj
            empleado.idPuesto      = puesto_obj
            empleado.idContrato    = contrato_obj
            empleado.Fecha_Ingreso = fecha_ingreso
            empleado.Activo        = activo_bool
            empleado.save()

        # Patrón PRG: evita reenvío del form al recargar
        return redirect('empleados')

    # ── GET: mostrar formulario + tabla ───────────────────
    return render(request, 'empleados.html', {
        'personas' : Persona.objects.order_by('Nombre_Completo'),
        'puestos'  : Puesto.objects.select_related('idDepartamento').order_by('Nombre'),
        'contratos': Contrato.objects.all(),
        'empleados': Empleado.objects.select_related(
                         'idPersona',
                         'idPuesto',
                         'idContrato'
                     ).order_by('idPersona__Nombre_Completo'),
    })


# =========================================================
# Vista: Editar Empleado
# Carga el formulario con los datos del empleado seleccionado
# =========================================================
def editar_empleado(request, id_empleado):

    empleado = get_object_or_404(Empleado, pk=id_empleado)

    if request.method == 'POST':
        empleado.idPersona     = Persona.objects.get(pk=request.POST.get('persona'))
        empleado.idPuesto      = Puesto.objects.get(pk=request.POST.get('puesto'))
        empleado.idContrato    = Contrato.objects.get(pk=request.POST.get('contrato'))
        empleado.Fecha_Ingreso = request.POST.get('fecha_ingreso')
        empleado.Activo        = request.POST.get('activo') == '1'
        empleado.save()

        return redirect('empleados')

    # GET: pre-rellena el formulario con los datos actuales
    return render(request, 'empleados.html', {
        'empleado_editar': empleado,
        'personas' : Persona.objects.order_by('Nombre_Completo'),
        'puestos'  : Puesto.objects.select_related('idDepartamento').order_by('Nombre'),
        'contratos': Contrato.objects.all(),
        'empleados': Empleado.objects.select_related(
                         'idPersona',
                         'idPuesto',
                         'idContrato'
                     ).order_by('idPersona__Nombre_Completo'),
    })


# =========================================================
# Vista: Eliminar Empleado
# =========================================================
def eliminar_empleado(request, id_empleado):
    empleado = get_object_or_404(Empleado, pk=id_empleado)
    empleado.delete()
    return redirect('empleados')



# =========================================================
# Vista: Pasantes — registro, modificación y listado
# =========================================================
def registrar_pasante(request):

    # ── POST: crear o modificar ────────────────────────────
    if request.method == 'POST':
        accion      = request.POST.get('accion')       # 'crear' o 'modificar'
        pasante_id  = request.POST.get('pasante_id')   # vacío si es nuevo

        persona_id      = request.POST.get('persona')
        puesto_id       = request.POST.get('puesto')
        supervisor_id   = request.POST.get('empleado_sup')
        fecha_inicio    = request.POST.get('fecha_inicio')
        fecha_fin       = request.POST.get('fecha_fin') or None # Maneja el null si viene vacío
        universidad     = request.POST.get('universidad')
        carrera         = request.POST.get('carrera')
        tutor_univ      = request.POST.get('tutor_universitario')
        activo          = request.POST.get('activo')           # '1' o '0'

        # Obtención de los objetos relacionados a través de las LLaves Foráneas
        persona_obj    = Persona.objects.get(pk=persona_id)
        puesto_obj     = Puesto.objects.get(pk=puesto_id)
        supervisor_obj = Empleado.objects.get(pk=supervisor_id)
        activo_bool    = activo == '1'

        if accion == 'crear' or not accion:
            Pasante.objects.create(
                idPersona           = persona_obj,
                idPuesto            = puesto_obj,
                idEmpleado_Sup      = supervisor_obj,
                Fecha_Inicio        = fecha_inicio,
                Fecha_Fin           = fecha_fin,
                Univercidad         = universidad, # Respetando la escritura exacta de tu modelo
                Carrera             = carrera,
                Tutor_Univercitario = tutor_univ,  # Respetando la escritura exacta de tu modelo
                Activo              = activo_bool,
            )

        elif accion == 'modificar' and pasante_id:
            pasante = Pasante.objects.get(pk=pasante_id)
            pasante.idPersona           = persona_obj
            pasante.idPuesto            = puesto_obj
            pasante.idEmpleado_Sup      = supervisor_obj
            pasante.Fecha_Inicio        = fecha_inicio
            pasante.Fecha_Fin           = fecha_fin
            pasante.Univercidad         = universidad
            pasante.Carrera             = carrera
            pasante.Tutor_Univercitario = tutor_univ
            pasante.Activo              = activo_bool
            pasante.save()

        # Patrón PRG: Redirección limpia para evitar duplicar el envío del formulario
        return redirect('pasantes')

    # ── GET: mostrar formulario + tabla ───────────────────
    return render(request, 'pasantes.html', {
        'personas': Persona.objects.order_by('Nombre_Completo'),
        'puestos' : Puesto.objects.order_by('Nombre'),
        
        # OBTENCIÓN DE SUPERVISORES: Trae todos los empleados con sus nombres para el select
        'supervisores': Empleado.objects.select_related('idPersona').order_by('idPersona__Nombre_Completo'),
        
        # LISTADO DE LA TABLA: Optimizado con select_related para evitar consultas lentas (N+1)
        'pasantes': Pasante.objects.select_related(
                        'idPersona', 
                        'idPuesto', 
                        'idEmpleado_Sup__idPersona' # Trae directamente la persona ligada al empleado supervisor
                    ).order_by('idPersona__Nombre_Completo'),
    })


# =========================================================
# Vista: Editar Pasante
# Carga el formulario con los datos del pasante seleccionado
# =========================================================
def editar_pasante(request, id_pasante):

    pasante = get_object_or_404(Pasante, pk=id_pasante)

    if request.method == 'POST':
        pasante.idPersona           = Persona.objects.get(pk=request.POST.get('persona'))
        pasante.idPuesto            = Puesto.objects.get(pk=request.POST.get('puesto'))
        pasante.idEmpleado_Sup      = Empleado.objects.get(pk=request.POST.get('empleado_sup'))
        pasante.Fecha_Inicio        = request.POST.get('fecha_inicio')
        pasante.Fecha_Fin           = request.POST.get('fecha_fin') or None
        pasante.Univercidad         = request.POST.get('universidad')
        pasante.Carrera             = request.POST.get('carrera')
        pasante.Tutor_Univercitario = request.POST.get('tutor_universitario')
        pasante.Activo              = request.POST.get('activo') == '1'
        pasante.save()

        return redirect('pasantes')

    # GET: Reutiliza la misma plantilla, inyectando 'pasante_editar' para rellenar los inputs
    return render(request, 'pasantes.html', {
        'pasante_editar': pasante,
        'personas'      : Persona.objects.order_by('Nombre_Completo'),
        'puestos'       : Puesto.objects.order_by('Nombre'),
        'supervisores'  : Empleado.objects.select_related('idPersona').order_by('idPersona__Nombre_Completo'),
        'pasantes'      : Pasante.objects.select_related(
                            'idPersona', 
                            'idPuesto', 
                            'idEmpleado_Sup__idPersona'
                        ).order_by('idPersona__Nombre_Completo'),
    })



# =========================================================
# Vista: Salarios — registro, modificación y listado
# =========================================================
def registrar_salario(request):

    if request.method == 'POST':

        accion = request.POST.get('accion')
        salario_id = request.POST.get('salario_id')

        empleado_id = request.POST.get('empleado')

        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        salario_bruto = Decimal(request.POST.get('salario_bruto') or 0)
        salario_sem_neto = Decimal(request.POST.get('salario_sem_neto') or 0)

        comision = Decimal(request.POST.get('comision_base') or 0)
        variable = Decimal(request.POST.get('variable_base') or 0)
        viaticos = Decimal(request.POST.get('viaticos_alimenticios') or 0)
        kilometraje = Decimal(request.POST.get('kilometraje_base') or 0)
        bono = Decimal(request.POST.get('bono_base') or 0)

        observaciones = request.POST.get('observaciones')

        empleado_obj = Empleado.objects.get(
            pk=empleado_id
        )

        if accion == 'crear' or not accion:

            print("POST COMPLETO:")
            print(request.POST)

            print("Fecha inicio:", fecha_inicio)
            print("Fecha fin:", fecha_fin)

            print("salario_bruto =", salario_bruto)
            print("salario_sem_neto =", salario_sem_neto)
            print("comision =", comision)
            print("variable =", variable)
            print("viaticos =", viaticos)
            print("kilometraje =", kilometraje)
            print("bono =", bono)

            SalarioEmpleado.objects.create(

                idEmpleado=empleado_obj,

                Fecha_Inicio=fecha_inicio,
                Fecha_Fin=fecha_fin if fecha_fin else None,

                Salario_Bruto=salario_bruto,
                Salario_Sem_Neto=salario_sem_neto,

                Comision_Base=comision,
                Variable_Base=variable,
                Viaticos_Alimenticios=viaticos,
                Kilometraje_Base=kilometraje,
                Bono_Base=bono,

                Observaciones=observaciones
            )

        elif accion == 'modificar' and salario_id:

            salario = SalarioEmpleado.objects.get(
                pk=salario_id
            )

            salario.idEmpleado = empleado_obj

            salario.Fecha_Inicio = fecha_inicio
            salario.Fecha_Fin = fecha_fin if fecha_fin else None

            salario.Salario_Bruto = salario_bruto
            salario.Salario_Sem_Neto = salario_sem_neto

            salario.Comision_Base = comision
            salario.Variable_Base = variable
            salario.Viaticos_Alimenticios = viaticos
            salario.Kilometraje_Base = kilometraje
            salario.Bono_Base = bono

            salario.Observaciones = observaciones

            salario.save()

        return redirect('salarios')

    return render(request, 'salario.html', {

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
    })


# =========================================================
# Vista: Editar Salario
# =========================================================
def editar_salario(request, id_salario):

    salario = get_object_or_404(
        SalarioEmpleado,
        pk=id_salario
    )

    return render(request, 'salario.html', {

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
    })


# =========================================================
# Obtener compensación base según el puesto del empleado
# =========================================================

def obtener_compensacion_empleado(request, id_empleado):

    try:

        empleado = Empleado.objects.select_related(
            'idPuesto'
        ).get(
            pk=id_empleado
        )

        print("EMPLEADO:", empleado)
        print("PUESTO:", empleado.idPuesto)
        print("ID PUESTO:", empleado.idPuesto.idPuesto)

        compensaciones = Compensacion_Puesto.objects.filter(
            idPuesto=empleado.idPuesto
        )

        print("COMPENSACIONES ENCONTRADAS:", compensaciones.count())

        compensacion = compensaciones.order_by(
            '-Vigencia'
        ).first()

        if compensacion is None:

            return JsonResponse({
                'success': False,
                'mensaje': 'El puesto no tiene compensación configurada.'
            })

        return JsonResponse({

            'success': True,

            'id_puesto': empleado.idPuesto.idPuesto,
            'puesto': empleado.idPuesto.Nombre,

            'salario_bruto':
                float(compensacion.Salario_Bruto),

            'salario_sem_neto':
                float(compensacion.Salario_Sem_Neto),

            'comision_base':
                float(compensacion.Comision_Base),

            'variable_base':
                float(compensacion.Variable_Base),

            'viaticos_alimenticios':
                float(compensacion.Viaticos_Alimenticios),

            'kilometraje_base':
                float(compensacion.Kilometraje_Base),

            'bono_base':
                float(compensacion.Bono_Base),

            'vigencia':
                compensacion.Vigencia.strftime('%Y-%m-%d')
                if compensacion.Vigencia else None

        })

    except Empleado.DoesNotExist:

        return JsonResponse({
            'success': False,
            'mensaje': 'Empleado no encontrado.'
        })

    except Exception as e:

        return JsonResponse({
            'success': False,
            'mensaje': str(e)
        })




def reclutamiento_view(request):
    return render(request, 'reclutamiento.html')

# =========================================================
# Registrar y Modificar Vacantes
# =========================================================
def registrar_vacante(request):

    if request.method == 'POST':

        accion = request.POST.get('accion')
        vacante_asig_id = request.POST.get('vacante_asig_id')

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
def registrar_candidato(request):

    if request.method == 'POST':

        accion = request.POST.get('accion')
        candidato_id = request.POST.get('candidato_id')

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
def registrar_solicitud_vacacion(request):

    if request.method == 'POST':

        accion = request.POST.get('accion')

        solicitud_id = request.POST.get('solicitud_id')


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
# GUARDAR CONSULTA DE VACACIONES
# =========================================================
def guardar_saldo_vacaciones(request):

    empleados = Empleado.objects.select_related(
        'idPersona'
    )

    if request.method == "POST":

        empleado_id = request.POST.get("empleado")

        empleado = Empleado.objects.get(
            idEmpleado=empleado_id
        )

        anio_actual = date.today().year

        saldo, creado = VacacionSaldo.objects.get_or_create(

            idEmpleado_Sal_Vac=empleado,

            Anio=anio_actual
        )

        for s in VacacionSolicitud.objects.filter(
            idEmpleado_Sol_Vac=empleado):
            print(
                s.idSolicitud,
                s.Dias_Solicitud,
                s.id_Estatus_Vacante.TipoEstatus
            )

        saldo.save()

    saldos = VacacionSaldo.objects.select_related(
        'idEmpleado_Sal_Vac',
        'idEmpleado_Sal_Vac__idPersona'
    )

    return render(
        request,
        'con_Vacacion.html',
        {
            'empleados': empleados,
            'saldos': saldos
        }
    )


# =========================================================
# MODIFICAR CONSULTA DE VACACIONES
# =========================================================
def editar_saldo_vacaciones(request, id):

    saldo = get_object_or_404(
        VacacionSaldo,
        idSaldo=id
    )

    if request.method == "POST":

        saldo.Anio = request.POST.get("anio")

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
# OBTENER EL SALDO DE VACACIONES
# =========================================================
def obtener_saldo_vacaciones(request):

    empleado_id = request.GET.get("empleado")

    empleado = Empleado.objects.get(
        idEmpleado=empleado_id
    )

    saldo = VacacionSaldo(
        idEmpleado_Sal_Vac=empleado,
        Anio=date.today().year
    )

    acumulados = saldo.calcular_dias_acumulados()

    tomados = saldo.calcular_dias_tomados()

    disponibles = acumulados - tomados

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
def guardar_asistencia(request):

    empleados = Empleado.objects.select_related(
        'idPersona'
    )

    estados = AsistenciaEstado.objects.all()

    if request.method == "POST":

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
def editar_asistencia(request, id):

    asistencia = get_object_or_404(

        Asistencia,

        idAsistencia=id

    )


    if request.method == "POST":

        asistencia.Fecha = request.POST.get("fecha")

        asistencia.Hora_Entrada = datetime.strptime(
            request.POST.get("hora_entrada"), "%H:%M"
        ).time()

        asistencia.Hora_Salida = datetime.strptime(
            request.POST.get("hora_salida"), "%H:%M"
        ).time()


        empleado = Empleado.objects.get(

            idEmpleado=request.POST.get("empleado")

        )

        asistencia.idEmpleado = empleado


        estado = AsistenciaEstado.objects.get(

            idAsis_Estado=request.POST.get("estado")

        )

        asistencia.idAsis_Estado = estado


        # Se recalculan las horas extra automáticamente
        asistencia.save()


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

            Justificacion=request.POST.get("justificacion"),

            id_TipoPermiso=tipo_permiso,

            idAsistencia=asistencia,

            idEmpleado=empleado
        )

        permiso.save()

        return redirect('guardar_permiso')


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
# GUARDAR CABECERA DE LA ACCIÓN DEL PERSONAL
# =========================================================
def registrar_cabecera_accion(request, pk=None):
    accion_cabecera = None
    paso_dos_habilitado = False

    # -------------------------------------------------------------------------
    # FLUJO GET: Si viene un PK en la URL, cargamos la cabecera existente (Paso 2)
    # -------------------------------------------------------------------------
    if pk:
        accion_cabecera = get_object_or_404(AccionPersonal, pk=pk)
        paso_dos_habilitado = True

    # -------------------------------------------------------------------------
    # FLUJO POST: Procesamiento de los dos formularios independientes
    # -------------------------------------------------------------------------
    if request.method == 'POST':
        action = request.POST.get('action')

        # === FORMULARIO 1: Iniciar Registro (Guardar Cabecera) ===
        if action == 'guardar_cabecera':
            form_cabecera = AccionPersonalForm(request.POST)
            if form_cabecera.is_valid():
                # Guarda en SQL Server y recupera la instancia con su ID autoincremental
                nueva_cabecera = form_cabecera.save()
                messages.success(request, f"Cabecera guardada con éxito. Folio: {nueva_cabecera.idAccion}")
                # Redirige a la ruta con el ID para desbloquear la segunda sección
                return redirect('gestionar_accion', pk=nueva_cabecera.idAccion)
            else:
                messages.error(request, "Error al validar los datos de la cabecera.")

        # === FORMULARIO 2: Aplicar y Sellar Acción (Guardar Detalle) ===
        elif action == 'finalizar_accion':
            # 1. Recuperamos el ID de la cabecera desde el input hidden del HTML
            id_cabecera_padre = request.POST.get('idAccion_padre')
            
            if not id_cabecera_padre:
                messages.error(request, "Error crítico: No se encontró la cabecera asociada al movimiento.")
                return redirect('crear_accion')

            # 2. Obtenemos el objeto de la cabecera real
            cabecera_obj = get_object_or_404(AccionPersonal, pk=id_cabecera_padre)

            # 3. Capturamos los datos enviados por el Formulario Detalle
            id_detalle_accion = request.POST.get('Tipo_Accion')  # ID del catálogo DetalleAccion
            id_salario_empleado = request.POST.get('idSalario')  # ID de SalarioEmpleado
            detalle_texto = request.POST.get('Detalle')

            # 4. Validamos que los campos obligatorios del HTML no vengan vacíos en el backend
            if not id_detalle_accion or not detalle_texto:
                messages.error(request, "Por favor complete todos los campos requeridos de la especificación.")
                return redirect('gestionar_accion', pk=cabecera_obj.idAccion)

            try:
                # 5. Instanciamos los objetos foráneos correspondientes
                catalogo_accion = get_object_or_404(DetalleAccion, pk=id_detalle_accion)
                
                # 'idSalarioEmpleado' puede ser opcional o nulo en algunos tipos de acciones
                salario_obj = None
                if id_salario_empleado:
                    salario_obj = get_object_or_404(SalarioEmpleado, pk=id_salario_empleado)

                # 6. Creamos y guardamos directamente en la tabla 'Accion_Tipo'
                nuevo_movimiento = AccionTipo(
                    idAccion=cabecera_obj,               # Instancia de AccionPersonal
                    id_Detalle_Accion=catalogo_accion,   # Instancia de DetalleAccion
                    idSalarioEmpleado=salario_obj,       # Instancia de SalarioEmpleado (o None)
                    Detalle=detalle_texto                # Texto libre (max_length=600)
                )
                
                # Ejecuta el INSERT en la base de datos SQL Server
                nuevo_movimiento.save()

                messages.success(request, f"El movimiento administrativo del Folio {cabecera_obj.idAccion} se ha sellado y guardado correctamente.")
                
                # Redirigimos al historial o pantalla principal de rotación
                return redirect('accion_rotacion')

            except Exception as e:
                messages.error(request, f"Error al guardar en la base de datos: {str(e)}")
                return redirect('gestionar_accion', pk=cabecera_obj.idAccion)

    else:
        # Si es un GET (Limpio o con PK), inicializamos el formulario de la cabecera
        form_cabecera = AccionPersonalForm(instance=accion_cabecera)

    
    empleados = Empleado.objects.select_related(
        'idPersona'
    ).all()

    for emp in empleados:

        salario = SalarioEmpleado.objects.filter(
            idEmpleado=emp
        ).order_by(
            '-idSalarioEmpleado'
        ).first()

        emp.salario_actual = (
            salario.Salario_Sem_Neto
            if salario else 0
        )

    # -------------------------------------------------------------------------
    # CONTEXTO: Pasamos los catálogos necesarios para los select del HTML
    # -------------------------------------------------------------------------
    context = {
        'form_cabecera': form_cabecera,
        'accion_cabecera': accion_cabecera,
        'paso_dos_habilitado': paso_dos_habilitado,
        'empleados': empleados,
        'tipos_accion': DetalleAccion.objects.all(),
        'salarios': SalarioEmpleado.objects.all(),

        # ✅ NUEVO: historial de acciones ya registradas (con detalle)
        'acciones': AccionTipo.objects.select_related(
            'idAccion',
            'id_Detalle_Accion',
            'idAccion__idEmpleado'
        ).order_by('-idAccion_Tipo'),
}
    
    return render(request, 'accion_Personal.html', context)


# =========================================================
# GUARDAR DETALLE DE LA ACCIÓN ANTERIORMENTE REGISTRADA
# =========================================================
def guardar_detalle_accion(request):

    if request.method == 'POST':

        id_accion = request.POST.get('idAccion_padre')

        cabecera = get_object_or_404(

            AccionPersonal,

            pk=id_accion
        )


        tipo_accion = get_object_or_404(

            DetalleAccion,

            pk=request.POST.get('Tipo_Accion')
        )


        descripcion = request.POST.get('Detalle')


        monto = None

        salario = None


        # ====================================
        # PREMIO
        # ====================================

        if tipo_accion.Accion == 'Premio':

            monto = Decimal(

                request.POST.get('monto_premio')
            )


        # ====================================
        # AJUSTE SALARIAL
        # ====================================

        elif tipo_accion.Accion == 'Ajuste Salarial':

            nuevo_salario = Decimal(

                request.POST.get('nuevo_salario')
            )


            salario = SalarioEmpleado.objects.filter(

                idEmpleado=cabecera.idEmpleado

            ).order_by(

                '-idSalarioEmpleado'

            ).first()


            if salario:

                salario.Salario_Sem_Neto = nuevo_salario

                salario.save()


            monto = nuevo_salario


        # ====================================
        # ASCENSO
        # ====================================

        elif tipo_accion.Accion == 'Ascenso':

            nuevo_salario = Decimal(

                request.POST.get('nuevo_salario')
            )


            salario = SalarioEmpleado.objects.filter(

                idEmpleado=cabecera.idEmpleado

            ).order_by(

                '-idSalarioEmpleado'

            ).first()


            if salario:

                salario.Salario_Sem_Neto = nuevo_salario

                salario.save()


            monto = nuevo_salario


        # ====================================
        # GUARDAR
        # ====================================

        movimiento = AccionTipo(

            idAccion=cabecera,

            id_Detalle_Accion=tipo_accion,

            Detalle=descripcion,

            Monto_TA=monto,

            idSalarioEmpleado=salario
        )

        movimiento.save()


        messages.success(

            request,

            "Acción registrada correctamente."
        )


        return redirect(

            'gestionar_accion',

            pk=cabecera.idAccion
        )


def obtener_salario_actual(request, idEmpleado):

    salario = SalarioEmpleado.objects.filter(
        idEmpleado=idEmpleado
    ).order_by(
        '-idSalarioEmpleado'
    ).first()

    if salario:

        return JsonResponse({

            'success': True,

            'salario': float(salario.Salario_Sem_Neto),

            'idSalario': salario.idSalarioEmpleado

        })

    return JsonResponse({

        'success': False,

        'salario': 0,

        'idSalario': None

    })


def rotacion_Personal_view(request):
    return render(request, 'rotacion_Personal.html')



def evaluaciones_view(request):
    return render(request, 'evaluaciones.html')


# =========================================================
# CREAR EVALUACIÓN + DESEMPEÑO (CABECERA + DETALLE)
# =========================================================
def crear_evaluacion(request):

    empleados = Empleado.objects.select_related("idPersona").all()
    evaluadores = Empleado.objects.select_related("idPersona").all()
    periodos = Periodo.objects.all()

    if request.method == "POST":

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

                total = sum([c1, c2, c3, c4, c5])
                pct_total = (total / 5) * 100

                EvaluacionDesempeno.objects.create(
                    Cumple_Metas_Objetivos=c1,
                    Cumple_FuncionesAsig=c2,
                    Entregables_Calidad_Tiempo=c3,
                    Cumple_Asistencia=c4,
                    Muestra_Compromiso_Colaboracion=c5,
                    pct_totalEv=pct_total,
                    idEvaluacion=evaluacion
                )

                messages.success(request, "Evaluación registrada correctamente.")
                return redirect("crear_evaluacion")

        except Exception as e:
            messages.error(request, f"Error al guardar: {str(e)}")

    context = {
        "empleados": empleados,
        "evaluadores": evaluadores,
        "periodos": periodos,
    }

    return render(request, "eva_Empleado.html", context)


# =========================================================
# CREAR EVALUACIÓN DE POTENCIAL (JEFATURA)
# =========================================================
def crear_evaluacion_jefatura(request):

    empleados = Empleado.objects.select_related("idPersona").all()
    evaluadores = Empleado.objects.select_related("idPersona").all()
    periodos = Periodo.objects.all()

    if request.method == "POST":

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
                liderazgo = request.POST.get("Capacidad_Liderazgo") == "1"
                aprendizaje = request.POST.get("Aprendizaje_Rapido") == "1"
                adaptacion = request.POST.get("Adaptacion_Cambio") == "1"
                iniciativa = request.POST.get("Iniciativa_Mejora") == "1"
                madurez = request.POST.get("Madurez_Emocional") == "1"

                observaciones = request.POST.get("Observaciones")

                # Calcular porcentaje
                total = sum([
                    liderazgo,
                    aprendizaje,
                    adaptacion,
                    iniciativa,
                    madurez
                ])

                pct_total = (total / 5) * 100

                # ====================================
                # GUARDAR DETALLE
                # ====================================
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

                return redirect("crear_evaluacion_jefatura")

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
def crear_matriz_9box(request):
    empleados = Empleado.objects.select_related("idPersona").all()
    periodos = Periodo.objects.all()
    perfiles = Cuadrante9BoxPerfil.objects.all()
    cuadrantes = Cuadrante9Box.objects.all()
    desempenos = Cuadrante9BoxDesempeno.objects.all()
    potenciales = Cuadrante9BoxPotencial.objects.all()

    if request.method == "POST":
        try:
            with transaction.atomic():
                # Asegúrate de mapear las llaves del POST exactas de tu formulario HTML
                UnionMatrizEmp.objects.create(
                    Anio=request.POST.get("Anio"),
                    Plan_Accion=request.POST.get("Plan_Accion"),
                    
                    # ⚠️ ¡CRUCIAL!: En tu HTML pusiste name="periodo"
                    idPeriodo_id=request.POST.get("periodo"),  
                    
                    # ⚠️ ¡CRUCIAL!: En tu HTML pusiste name="idCuadrante_9box"
                    idCuadrante_9box_id=request.POST.get("idCuadrante_9box"),  
                    
                    # Verificados con tus etiquetas <select name="..."> del formulario de configuración:
                    idCuadrante_9box_Perfil_id=request.POST.get("idCuadrante_9box_Perfil"),
                    idCuadrante_9box_Desempeno_id=request.POST.get("idCuadrante_9box_Desempeno"),
                    idCuadrante_9box_Potencial_id=request.POST.get("idCuadrante_9box_Potencial"),
                    idEmpleado_id=request.POST.get("idEmpleado")
                )

                messages.success(request, "Matriz 9 Box registrada correctamente.")
                return redirect("crear_matriz_9box")

        except Exception as e:
            messages.error(request, f"Error al guardar: {str(e)}")

    context = {
        "empleados": empleados,
        "periodos": periodos,
        "perfiles": perfiles,
        "cuadrantes": cuadrantes,
        "desempenos": desempenos,
        "potenciales": potenciales,
    }
    return render(request, "matriz.html", context)


# =========================================================
# DASHBOARD RESULTADOS (CON PORCENTAJE DE DESEMPEÑO INTEGRADO)
# =========================================================
def dashboard_resultados(request):
    # 1. Cargamos catálogos para renderizar los selectores
    empleados = Empleado.objects.select_related("idPersona").all()
    periodos = Periodo.objects.all()
    
    # 2. Capturamos los tres filtros obligatorios mediante el método GET
    empleado_filtro = request.GET.get('empleado_filtro')
    periodo_filtro = request.GET.get('periodo_filtro')
    anio_filtro = request.GET.get('anio_filtro') # Capturamos el Año
    
    matriz_seleccionada = None
    potencial_seleccionado = None
    porcentaje_desempeno = None  # Variable para almacenar el % calculado

    # 3. Solo si el usuario llenó los tres criterios realizamos la consulta consolidada
    if empleado_filtro and periodo_filtro and anio_filtro:
        try:
            # A. Buscamos el registro en la matriz cruzando empleado, periodo y año
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
                messages.warning(request, "No se encontraron resultados de la Matriz 9 Box para los criterios seleccionados.")
            
            # =========================================================
            # B. Buscamos la evaluación de potencial y el desempeño asociado
            # =========================================================
            registros_potencial = EvaluacionJefePotencial.objects.select_related('idEvaluacion').all()
            
            for pot in registros_potencial:
                eval_obj = pot.idEvaluacion
                if not eval_obj:
                    continue
                
                # 1. Extraer ID del Empleado dinámicamente
                eval_emp_id = None
                for attr in ['idEmpleado_id', 'idEmpleado', 'empleado_id', 'empleado']:
                    if hasattr(eval_obj, attr):
                        val = getattr(eval_obj, attr)
                        eval_emp_id = val.idEmpleado if hasattr(val, 'idEmpleado') else val
                        break
                
                # 2. Extraer ID del Periodo dinámicamente
                eval_per_id = None
                for attr in ['idPeriodo_id', 'idPeriodo', 'periodo_id', 'periodo']:
                    if hasattr(eval_obj, attr):
                        val = getattr(eval_obj, attr)
                        eval_per_id = val.idPeriodo if hasattr(val, 'idPeriodo') else val
                        break

                # 3. Extraer el Año dinámicamente
                eval_anio = None
                if hasattr(eval_obj, 'Anio'):
                    eval_anio = eval_obj.Anio
                elif hasattr(eval_obj, 'anio'):
                    eval_anio = eval_obj.anio
                elif eval_obj.idPeriodo and hasattr(eval_obj.idPeriodo, 'Anio'):
                    eval_anio = eval_obj.idPeriodo.Anio

                # Validamos coincidencia estricta
                if (str(eval_emp_id) == str(empleado_filtro) and 
                    str(eval_per_id) == str(periodo_filtro) and 
                    str(eval_anio) == str(anio_filtro)):
                    
                    potencial_seleccionado = pot
                    
                    # 4. Buscamos el porcentaje de desempeño asociado a esta misma evaluación
                    desempeno_obj = EvaluacionDesempeno.objects.filter(idEvaluacion=eval_obj).first()
                    if desempeno_obj:
                        porcentaje_desempeno = desempeno_obj.pct_totalEv
                    
                    break # Salimos del bucle al encontrar los datos correctos
            
        except Exception as e:
            messages.error(request, f"Error al consultar los datos: {str(e)}")

    # 4. Construimos el contexto para el HTML
    context = {
        'empleados': empleados,
        'periodos': periodos,
        'matriz_seleccionada': matriz_seleccionada,
        'potencial_seleccionado': potencial_seleccionado, 
        'porcentaje_desempeno': porcentaje_desempeno, # Enviado al template HTML
        
        # Guardamos las selecciones para mantener fijos los campos tras recargar la pantalla
        'empleado_filtro_id': None,
        'periodo_filtro_id': None,
        'anio_filtro_val': anio_filtro if anio_filtro else "",
    }
    
    # Manejo preventivo para evitar errores de casteo int()
    try:
        if empleado_filtro: context['empleado_filtro_id'] = int(empleado_filtro)
        if periodo_filtro: context['periodo_filtro_id'] = int(periodo_filtro)
    except ValueError:
        pass
        
    return render(request, 'result_Evaluacion.html', context)



def elec_KPI_view(request):
    return render(request, 'elec_KPI.html')


# =========================================================================
# 1. VISTA SÓLO PARA LA CABECERA (Carga inicial y Guardado de Cabecera)
# =========================================================================
def registrar_kpi_view(request):
    kpi_cabecera_id = None
    el_empleado_seleccionado = ""
    el_mes_seleccionado = ""
    el_anio_seleccionado = "2026"

    if request.method == 'POST':
        id_empleado = request.POST.get('idEmpleado')
        mes = request.POST.get('Mes')
        anio = request.POST.get('Anio')

        # Mantener el estado en los inputs si ocurre un error (conversión segura)
        el_empleado_seleccionado = int(id_empleado) if id_empleado else ""
        el_mes_seleccionado = int(mes) if mes else ""
        el_anio_seleccionado = int(anio) if anio else 2026

        try:
            empleado = Empleado.objects.get(pk=id_empleado)
            
            # Crear y guardar la cabecera adaptada a enteros de models.py
            cabecera = KpiCabecera(
                idEmpleado=empleado,
                mes=int(mes),    # Adaptado a models.IntegerField
                anio=int(anio)   # Adaptado a models.IntegerField
            )
            cabecera.save()

            kpi_cabecera_id = cabecera.id_KPI
            messages.success(request, f"¡Cabecera registrada con éxito! ID Asignado: {kpi_cabecera_id}")

        except IntegrityError:
            messages.error(request, "Error: Ya existe un registro de KPI para este colaborador en el mes y año seleccionados.")
        except Empleado.DoesNotExist:
            messages.error(request, "El colaborador seleccionado no es válido.")
        except (ValueError, TypeError):
            messages.error(request, "Error: Los datos de mes o año enviados no son válidos.")

    # Catálogos necesarios para renderizar el formulario
    empleados = Empleado.objects.filter(Activo=True)
    categorias = KpiCategoria.objects.all()

    context = {
        'empleados': empleados,
        'categorias': categorias,
        'kpi_cabecera_id': kpi_cabecera_id,
        'el_empleado_seleccionado': el_empleado_seleccionado,
        'el_mes_seleccionado': el_mes_seleccionado,
        'el_anio_seleccionado': el_anio_seleccionado,
    }
    return render(request, 'kpi_Registro.html', context)


# =========================================================================
# 2. VISTA SÓLO PARA AGREGAR EL DETALLE (Procesamiento independiente)
# =========================================================================
def registrar_kpi_detalle_view(request):
    if request.method == 'POST':
        id_kpi_cabecera = request.POST.get('id_KPI')
        id_categoria = request.POST.get('id_KPI_Categoria')
        pct_alcanzado = request.POST.get('pct_Alcanzado')
        monto_base = request.POST.get('Monto_Base')

        try:
            cabecera = get_object_or_404(KpiCabecera, pk=id_kpi_cabecera)
            categoria = get_object_or_404(KpiCategoria, pk=id_categoria)

            # Cálculo manual de respaldo antes de insertar
            monto_total = float(monto_base) * (float(pct_alcanzado) / 100.0)

            # Crear y registrar el detalle vinculado a las FKs correctas
            detalle = KpiDetalle(
                id_KPI=cabecera,                       # Instancia de KpiCabecera
                id_KPI_Categoria=categoria,             # Instancia de KpiCategoria
                pct_Alcanzado=float(pct_alcanzado),     # Adaptado a DecimalField
                Monto_Base=float(monto_base),           # Adaptado a DecimalField
                Monto_Total=round(monto_total, 2)       # Redondeado a 2 decimales para DecimalField
            )
            detalle.save()
            
            messages.success(request, f"Indicador '{categoria.tipo_categoria}' añadido exitosamente.")

        except IntegrityError:
            # Captura la restricción UQ_KPI_Categoria_Por_Mes de tu Meta class
            messages.error(request, "Error: Esta categoría ya fue evaluada en este mes para el colaborador.")
        except Exception as e:
            messages.error(request, f"Error al guardar el detalle: {str(e)}")

    # Después de procesar el detalle, volvemos al flujo principal
    return redirect('registrar_kpi')

def crear_premio(request):
    if request.method == 'POST':
        form = PremioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Premio guardado exitosamente!')
            return redirect('crear_premio')
    else:
        form = PremioForm()

    premios = Premio.objects.select_related(
        'id_KPI_Categoria',
        'idCuadrante_9box_Perfil'
    ).all().order_by('idPremio')

    return render(
        request,
        'kpi_Premio.html',
        {
            'form': form,
            'premios': premios,
        }
    )


def editar_premio(request, id):
    premio = Premio.objects.get(pk=id)

    if request.method == 'POST':
        form = PremioForm(request.POST, instance=premio)

        if form.is_valid():
            form.save()
            messages.success(request, "Premio actualizado correctamente.")
            return redirect('crear_premio')

    else:
        form = PremioForm(instance=premio)

    premios = Premio.objects.select_related(
        'id_KPI_Categoria',
        'idCuadrante_9box_Perfil'
    ).order_by('idPremio')

    return render(
        request,
        'kpi_Premio.html',
        {
            'form': form,
            'premios': premios,
        }
    )



def crear_premio_asignado(request):

    if request.method == "POST":

        form = PremioAsignadoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Premio asignado correctamente."
            )
            return redirect("crear_premio_asignado")

    else:
        form = PremioAsignadoForm(
            initial={
                "Fecha_Registro": timezone.now().date()
            }
        )

    premios_asignados = (
        PremioAsignado.objects
        .select_related(
            "idPremio",
            "id_KPI",
            "id_KPI__idEmpleado"
        )
        .order_by("-Fecha_Registro")
    )

    context = {
        "form": form,
        "premios_asignados": premios_asignados,
    }

    return render(
        request,
        "kpi_AsigPremio.html",
        context
    )


# =========================================================================
# VISTA: Dashboard / Historial de KPIs
# =========================================================================
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
    total_kpis      = detalles.count()
    total_bonos     = detalles.aggregate(t=Sum('Monto_Total'))['t'] or 0
    pct_promedio    = detalles.aggregate(p=Avg('pct_Alcanzado'))['p'] or 0

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
        # Catálogos
        'empleados'           : empleados,
        'categorias'          : categorias,
        # Filtros activos
        'empleado_filtro_id'  : empleado_filtro_id,
        'mes_filtro'          : mes_filtro,
        'anio_filtro'         : anio_filtro,
        # Historial
        'detalles'            : detalles,
        'premios_qs'          : premios_qs,
        # Estadísticas
        'total_kpis'          : total_kpis,
        'total_bonos'         : total_bonos,
        'pct_promedio'        : round(pct_promedio, 2),
        'total_premios'       : total_premios,
        # Rankings
        'top_colaboradores'   : top_colaboradores,
        'resumen_financiero'  : resumen_financiero,
        # Meses para el select
        'meses': [
            (1,'Enero'),(2,'Febrero'),(3,'Marzo'),(4,'Abril'),
            (5,'Mayo'),(6,'Junio'),(7,'Julio'),(8,'Agosto'),
            (9,'Septiembre'),(10,'Octubre'),(11,'Noviembre'),(12,'Diciembre'),
        ],
    }

    return render(request, 'kpi.html', context)







def usuarios_view(request):
    return render(request, 'usuarios.html')

def configuraciones_view(request):
    return render(request, 'configuraciones.html')

def reportes_view(request):
    return render(request, 'reportes.html')









def onboarding_view(request):
    return render(request, 'onboarding.html')







def elec_Offboarding_view(request):
    return render(request, 'elec_Offboarding.html')

def registrar_off_view(request):
    return render(request, 'registrar_off.html')

def checklist_off_view(request):
    return render(request, 'checklist_off.html')

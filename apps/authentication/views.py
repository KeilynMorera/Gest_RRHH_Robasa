from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from decimal import Decimal

from .models import (
    Persona,
    PersonaSexo,
    Empresa,
    Gerencia,
    Departamento,
    Puesto,
    Compensacion_Puesto,
    Contrato,
    Empleado,
    Pasante,
    SalarioEmpleado,
)

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

    return render(request, 'salarios.html', {

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


def vacaciones_view(request):
    return render(request, 'vacaciones.html')

def sol_Vacacion_view(request):
    return render(request, 'sol_Vacacion.html')

def con_Vacacion_view(request):
    return render(request, 'con_Vacacion.html')

def elec_Asistencia_view(request):
    return render(request, 'elec_Asistencia.html')

def asistencia_view(request):
    return render(request, 'asistencia.html')

def permiso_view(request):
    return render(request, 'permiso.html')

def evaluaciones_view(request):
    return render(request, 'evaluaciones.html')

def eva_Empleado_view(request):
    return render(request, 'eva_Empleado.html')

def eva_Jefatura_view(request):
    return render(request, 'eva_Jefatura.html')

def result_Evaluacion_view(request):
    return render(request, 'result_Evaluacion.html')

def matriz_view(request):
    return render(request, 'matriz.html')

def reclutamiento_view(request):
    return render(request, 'reclutamiento.html')

def vacante_view(request):
    return render(request, 'vacante.html')

def reclut_Vacante_view(request):
    return render(request, 'reclut_Vacante.html')

def usuarios_view(request):
    return render(request, 'usuarios.html')

def configuraciones_view(request):
    return render(request, 'configuraciones.html')

def reportes_view(request):
    return render(request, 'reportes.html')

def elec_KPI_view(request):
    return render(request, 'elec_KPI.html')

def kpi_Registro_view(request):
    return render(request, 'kpi_Registro.html')

def kpi_Detalle_view(request):
    return render(request, 'kpi_Detalle.html')

def kpi_Premio_view(request):
    return render(request, 'kpi_Premio.html')

def kpi_view(request):
    return render(request, 'kpi.html')

def onboarding_view(request):
    return render(request, 'onboarding.html')

def accion_rotacion_view(request):
    return render(request, 'accion_rotacion.html')

def accion_Personal_view(request):
    return render(request, 'accion_Personal.html')

def rotacion_Personal_view(request):
    return render(request, 'rotacion_Personal.html')

def elec_Offboarding_view(request):
    return render(request, 'elec_Offboarding.html')

def registrar_off_view(request):
    return render(request, 'registrar_off.html')

def checklist_off_view(request):
    return render(request, 'checklist_off.html')

def kpi_AsigPremio_view(request):
    return render(request, 'kpi_AsigPremio.html')
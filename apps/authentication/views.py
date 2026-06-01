from django.shortcuts import render, redirect, get_object_or_404
from .models import Persona, PersonaSexo, Empresa

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
# Vista: Elección Personas o Empleados
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
# Vista: Empresas — registro, modificación y listado
# NOTA: esta función reemplaza tanto 'registrar_empresa'
#       como 'empresas_view'. En urls.py debe quedar
#       una sola ruta apuntando aquí con name='empresas'.
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

        # ==========================
        # CREAR EMPRESA
        # ==========================
        if accion == 'crear' or not accion:

            Empresa.objects.create(
                Nombre=nombre_empresa,
                Descripcion=descripcion_empresa
            )

        # ==========================
        # MODIFICAR EMPRESA
        # ==========================
        elif accion == 'modificar' and empresa_id:

            empresa = Empresa.objects.get(pk=empresa_id)

            empresa.Nombre = nombre_empresa
            empresa.Descripcion = descripcion_empresa

            empresa.save()

        return redirect('empresas')

    # ─────────────────────────────────────────────
    # GET → Mostrar formulario + listado
    # ─────────────────────────────────────────────
    return render(request, 'empresas.html', {
        'empresas': Empresa.objects.all().order_by('Nombre')
    })


def editar_empresa(request, idEmpresa):

    empresa = get_object_or_404(Empresa, pk=idEmpresa)

    return render(request, 'empresas.html', {
        'empresa_editar': empresa,
        'empresas': Empresa.objects.all().order_by('Nombre')
    })


# =========================================================
# Resto de vistas (sin cambios)
# =========================================================
def empleados_view(request):
    return render(request, 'empleados.html')

def pasantes_view(request):
    return render(request, 'pasantes.html')

def comple_Empresa_view(request):
    return render(request, 'comple_Empresa.html')

def gerencia_view(request):
    return render(request, 'gerencia.html')

def departamento_view(request):
    return render(request, 'departamento.html')

def puesto_view(request):
    return render(request, 'puesto.html')

def confi_Puesto_view(request):
    return render(request, 'confi_Puesto.html')

def salario_view(request):
    return render(request, 'salario.html')

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
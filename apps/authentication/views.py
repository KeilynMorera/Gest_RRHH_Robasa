#render() busca el archivo base.html.
from django.shortcuts import render, redirect

#render() busca el arcchivo models.py para traer los datos de la base de datos.
from .models import Persona, PersonaSexo

#Se procesa. Lo envía al navegador como HTML.
def home(request):
    return render(request, 'login.html')

#Pagina de inicio
def inicio_view(request):
    return render(request, 'inicio.html')

#Pagina de eleción (Personas o Empleados)
def per_emp_view(request):
    return render(request, 'per_emp.html')

#Pagina de registro de empleados
def empleados_view(request):
    return render(request, 'empleados.html')


#Pagina de registro de pasantes
def pasantes_view(request):
    return render(request, 'pasantes.html')

#Pagina de registro de empresas
def empresas_view(request):
    return render(request, 'empresas.html')

#Pagina de eleción (Gerencia o Departamento y Puesto)
def comple_Empresa_view(request):
    return render(request, 'comple_Empresa.html')

#Pagina de registro de gerencia
def gerencia_view(request):
    return render(request, 'gerencia.html')

#Pagina de registro de departamento
def departamento_view(request):
    return render(request, 'departamento.html')

#Pagina de registro de puesto
def puesto_view(request):
    return render(request, 'puesto.html')

#Pagina de configuración del puesto
def confi_Puesto_view(request):
    return render(request, 'confi_Puesto.html')

#Pagina de registro salarial
def salario_view(request):
    return render(request, 'salario.html')

#Pagina de eleción (Solicitud o Consulta de Vacaciones)
def vacaciones_view(request):
    return render(request, 'vacaciones.html')

#Pagina de registro solicitud de vacaciones
def sol_Vacacion_view(request):
    return render(request, 'sol_Vacacion.html')

#Pagina de registro solicitud de vacaciones
def con_Vacacion_view(request):
    return render(request, 'con_Vacacion.html')

#Pagina de eleción (Asistencia o Permiso)
def elec_Asistencia_view(request):
    return render(request, 'elec_Asistencia.html')

#Pagina de registro de Asistencia
def asistencia_view(request):
    return render(request, 'asistencia.html')

#Pagina de registro de Permiso
def permiso_view(request):
    return render(request, 'permiso.html')

#Pagina de eleción (Evaluación de Empleado Corriente o Jefatura)
def evaluaciones_view(request):
    return render(request, 'evaluaciones.html')

#Pagina de registro de Evaluación Empleado
def eva_Empleado_view(request):
    return render(request, 'eva_Empleado.html')

#Pagina de registro de Evaluación Jefatura
def eva_Jefatura_view(request):
    return render(request, 'eva_Jefatura.html')

#Pagina de ver los resultados de la correspondiente evaluación
def result_Evaluacion_view(request):
    return render(request, 'result_Evaluacion.html')

#Pagina de registro de la evaluación de la matriz
def matriz_view(request):
    return render(request, 'matriz.html')

#Pagina de eleción (Registro Vantante (para publicación) o
# Vacante candidato (para ingresar el empleado o persona interesado))
def reclutamiento_view(request):
    return render(request, 'reclutamiento.html')

#Pagina de registro de vacante abierta
def vacante_view(request):
    return render(request, 'vacante.html')

#Pagina de registro de candidato a la vacante
def reclut_Vacante_view(request):
    return render(request, 'reclut_Vacante.html')

#Pagina de registro de los usuarios con permisos de usar el sistema
def usuarios_view(request):
    return render(request, 'usuarios.html')

#Pagina de configuraciones para el sistema
def configuraciones_view(request):
    return render(request, 'configuraciones.html')

#Pagina de generación de reportes
def reportes_view(request):
    return render(request, 'reportes.html')

#Pagina de eleción (Seleccione un "componente" de KPI)
def elec_KPI_view(request):
    return render(request, 'elec_KPI.html')

#Pagina de Registro KPI
def kpi_Registro_view(request):
    return render(request, 'kpi_Registro.html')

#Pagina de Detalle KPI
def kpi_Detalle_view(request):
    return render(request, 'kpi_Detalle.html')

#Pagina de Premio KPI
def kpi_Premio_view(request):
    return render(request, 'kpi_Premio.html')

#Pagina de Resumen KPIs
def kpi_view(request):
    return render(request, 'kpi.html')

#Pagina de Oboarding
def onboarding_view(request):
    return render(request, 'onboarding.html')

#Pagina de Acciones o Rotaciones Personal
def accion_rotacion_view(request):
    return render(request, 'accion_rotacion.html')

#Pagina de Acciones de Personal
def accion_Personal_view(request):
    return render(request, 'accion_Personal.html')

#Pagina de Rotaciones de Personal
def rotacion_Personal_view(request):
    return render(request, 'rotacion_Personal.html')

#Pagina de Elección de Offboarding
def elec_Offboarding_view(request):
    return render(request, 'elec_Offboarding.html')

#Pagina de Registrar Offboarding
def registrar_off_view(request):
    return render(request, 'registrar_off.html')

#Pagina de Checklist de Offboarding
def checklist_off_view(request):
    return render(request, 'checklist_off.html')

#Pagina de Asignar Premios a KPIs
def kpi_AsigPremio_view(request):   
    return render(request, 'kpi_AsigPremio.html')


###################################### Enviar Registros ######################################

def registrar_persona(request):

    # Traer sexos desde la BD
    sexos = PersonaSexo.objects.all()

    # Si el formulario fue enviado
    if request.method == 'POST':

        nombre = request.POST.get('nombre_completo')
        cedula = request.POST.get('cedula')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        telefono = request.POST.get('telefono')
        celular = request.POST.get('celular')
        correo = request.POST.get('correo')
        direccion = request.POST.get('direccion')

        # Foreign Key
        sexo_id = request.POST.get('sexo')
        sexo = PersonaSexo.objects.get(idSexo=sexo_id)

        # Foto
        foto = request.FILES.get('foto')

        # Guardar en BD
        Persona.objects.create(
            Nombre=nombre,
            Cedula=cedula,
            Fecha_Nacimiento=fecha_nacimiento,
            Telefono=telefono,
            Celular=celular,
            Correo=correo,
            Direccion=direccion,
            Foto=foto,
            idSexo=sexo
        )

        # Redireccionar
        return redirect('per_emp')

    # Mostrar formulario
    return render(
        request,
        'personas.html',
        {
            'sexos': sexos
        }
    )


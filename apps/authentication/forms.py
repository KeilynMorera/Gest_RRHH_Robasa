from django import forms
from itertools import groupby

from .models import *

# ==============================================================================
# FORMULARIO: REGISTRO Y CABECERA DE ACCIONES DE PERSONAL
# ==============================================================================
class AccionPersonalForm(forms.ModelForm):
    """
    Formulario basado en el modelo `AccionPersonal` para la gestión y registro 
    de las cabeceras de movimientos o acciones de personal por empleado.

    Atributos principales:
        - idEmpleado: Selector dinámico con etiqueta personalizada (Nombre Completo).
        - Fecha: Selector HTML5 de fecha (`type='date'`).

    Optimizaciones:
        - Aplica `select_related('idPersona')` en la inicialización para evitar la 
          consulta N+1 al renderizar el listado de colaboradores.
    """

    class Meta:
        model = AccionPersonal
        fields = ['idEmpleado', 'Fecha']
        widgets = {
            'idEmpleado': forms.Select(attrs={
                'class': 'form-control', 
                'id': 'idEmpleado'
            }),
            'Fecha': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control', 
                'id': 'Fecha'
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Personaliza la consulta y presentación de las opciones del campo `idEmpleado`.
        """
        super().__init__(*args, **kwargs)
        
        # Carga optimizada del QuerySet incluyendo la relación de Persona en una sola consulta SQL
        self.fields['idEmpleado'].queryset = Empleado.objects.select_related('idPersona').all()
        
        # Formatea el texto visible de cada opción del selector para mostrar el nombre completo
        self.fields['idEmpleado'].label_from_instance = lambda obj: f"{obj.idPersona.Nombre_Completo}"



# ==============================================================================
# FORMULARIO: REGISTRO Y CONFIGURACIÓN DE PREMIOS / INCENTIVOS
# ==============================================================================
class PremioForm(forms.ModelForm):
    """
    Formulario basado en el modelo `Premio` para la creación y gestión de incentivos 
    asociados a categorías de KPI y perfiles de evaluación de la Matriz 9-Box.

    Atributos principales:
        - Descripcion: Texto descriptivo del incentivo o reconocimiento.
        - Alcance: Nivel de aplicación del premio (ej. Departamental, Regional, Global).
        - Monto: Valor monetario numérico asignado con precisión de decimales.
        - id_KPI_Categoria: Selector dinámico de la categoría de KPI asociada.
        - idCuadrante_9box_Perfil: Selector dinámico del cuadrante del perfil 9-Box elegible.

    Personalizaciones:
        - Asignación de etiquetas amigables (`labels`) para la interfaz de usuario.
        - Estilizado de widgets con clases Bootstrap (`form-control`) y marcadores de posición (`placeholders`).
        - Personalización de las etiquetas predeterminadas (`empty_label`) en campos de selección única.
    """

    class Meta:
        model = Premio
        fields = [
            'Descripcion', 
            'Alcance', 
            'Monto', 
            'id_KPI_Categoria', 
            'idCuadrante_9box_Perfil'
        ]
        
        # Define etiquetas personalizadas para la renderización de campos en el template
        labels = {
            'Descripcion': 'Descripción del Premio',
            'Alcance': 'Alcance',
            'Monto': 'Monto Monetario',
            'id_KPI_Categoria': 'Categoría de KPI',
            'idCuadrante_9box_Perfil': 'Perfil Cuadrante 9-Box',
        }
        
        # Aplica widgets HTML5 con atributos de diseño y validación
        widgets = {
            'Descripcion': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: Premio al Vendedor del Mes'
            }),
            'Alcance': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: Departamental, Regional...'
            }),
            'Monto': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01', 
                'placeholder': '0.00'
            }),
            'id_KPI_Categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'idCuadrante_9box_Perfil': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Inicializador del formulario para personalizar opciones estéticas y
        textos predeterminados de los selectores desplegables (`Select`).
        """
        super().__init__(*args, **kwargs)
        
        # Modifica el texto por defecto de la opción nula/vacía en los selectores
        self.fields['id_KPI_Categoria'].empty_label = "Seleccione una categoría..."
        self.fields['idCuadrante_9box_Perfil'].empty_label = "Seleccione un perfil..."



# ==============================================================================
# FORMULARIO: ASIGNACIÓN DE PREMIOS A EVALUACIONES DE KPI
# ==============================================================================
class PremioAsignadoForm(forms.ModelForm):
    """
    Formulario basado en el modelo `PremioAsignado` para la vinculación e 
    historial de premios otorgados a colaboradores según sus evaluaciones de KPI.

    Atributos principales:
        - id_KPI: Instancia de evaluación en `KpiCabecera` a la que se adjudica el premio.
        - idPremio: Catálogo de incentivo/premio seleccionado para la asignación.
        - Fecha_Registro: Fecha efectiva en la que se registra el otorgamiento del premio.

    Optimizaciones:
        - Utiliza `select_related` para precargar relaciones clave en las consultas SQL 
          evitando problemas de rendimiento (N+1) al procesar listados.
    """

    class Meta:
        model = PremioAsignado

        # =========================================================
        # 1. CAMPOS EXPUESTOS EN EL FORMULARIO
        # =========================================================
        fields = [
            'id_KPI',
            'idPremio',
            'Fecha_Registro',
        ]

        # =========================================================
        # 2. CONFIGURACIÓN DE WIDGETS Y CLASES DE DISEÑO
        # =========================================================
        widgets = {
            # Selector de la cabecera de KPI evaluado
            'id_KPI': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'id_KPI'
                }
            ),

            # Selector del premio/incentivo disponible
            'idPremio': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'idPremio'
                }
            ),

            # Selector de fecha HTML5 en formato estándar ISO (YYYY-MM-DD)
            'Fecha_Registro': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'id': 'id_Fecha_Registro'
                }
            ),
        }

    # =============================================================
    # 3. INICIALIZACIÓN Y CONFIGURACIÓN DINÁMICA DE CAMPOS
    # =============================================================
    def __init__(self, *args, **kwargs):
        """
        Personaliza los QuerySets de los selectores para optimizar las consultas a la BD,
        ordena la información para el usuario y establece las etiquetas y reglas de validación.
        """
        super().__init__(*args, **kwargs)

        # ── Carga y optimización del selector de KPIs ─────────────────────
        # Se precargan 'idEmpleado' y 'idPersona' para construir etiquetas de texto sin consultas extra.
        # Ordenado por periodo más reciente (Año -> Mes descendente).
        self.fields['id_KPI'].queryset = (
            KpiCabecera.objects
            .select_related(
                'idEmpleado',
                'idEmpleado__idPersona'
            )
            .all()
            .order_by(
                '-anio',
                '-mes'
            )
        )

        # ── Carga y optimización del selector de Premios ──────────────────
        # Precarga la relación con 'id_KPI_Categoria' y ordena alfabéticamente por descripción.
        self.fields['idPremio'].queryset = (
            Premio.objects
            .select_related(
                'id_KPI_Categoria'
            )
            .all()
            .order_by(
                'Descripcion'
            )
        )

        # ── Asignación de etiquetas personalizadas (Labels) ───────────────
        self.fields['id_KPI'].label = 'Registro KPI Evaluado'
        self.fields['idPremio'].label = 'Premio Asociado'
        self.fields['Fecha_Registro'].label = 'Fecha de Registro'

        # ── Definición de reglas de requerimiento estricto ────────────────
        self.fields['id_KPI'].required = True
        self.fields['idPremio'].required = True
        self.fields['Fecha_Registro'].required = True



# ==============================================================================
# CAMPO PERSONALIZADO DE FORMULARIO: SELECTOR DE EMPLEADO CON DEPARTAMENTO
# ==============================================================================
class EmpleadoConDepartamentoField(forms.ModelChoiceField):
    """
    Campo de selección personalizado derivado de `ModelChoiceField` diseñado para
    representar instancias de `Empleado` en formularios de Django.

    Propósito:
        Sobrescribir la representación en texto (`label`) de cada opción dentro del 
        HTML `<select>` para mostrar tanto el nombre completo del colaborador 
        como el nombre del departamento al que pertenece.

    Requisito de rendimiento:
        Al utilizar este campo en un formulario, asegúrate de aplicar `select_related` 
        en la consulta del QuerySet original para evitar el problema de consultas N+1:
        `Empleado.objects.select_related('idPersona', 'idPuesto__idDepartamento')`
    """

    def label_from_instance(self, obj):
        """
        Determina la etiqueta formateada que se mostrará para cada objeto `Empleado` 
        en las opciones del selector desplegable.

        Argumentos:
            obj (Empleado): Instancia individual del modelo Empleado.

        Retorna:
            str: Cadena formateada con la estructura "Nombre Completo — Departamento".
        """
        return (
            f"{obj.idPersona.Nombre_Completo} "
            f"— {obj.idPuesto.idDepartamento.Nombre}"
        )



# ==============================================================================
# FORMULARIO: REGISTRO Y GESTIÓN DE ONBOARDING DE EMPLEADOS
# ==============================================================================
class OnboardingForm(forms.ModelForm):
    """
    Formulario basado en el modelo `Onboarding` para la creación y edición 
    de procesos de incorporación.

    Incluye lógica dinámica en `__init__` para filtrar la lista de empleados 
    según el departamento asociado cuando se edita un registro existente.
    """

    # Selector de empleado formateado y optimizado
    idEmpleado = EmpleadoConDepartamentoField(
        queryset=Empleado.objects.select_related(
            "idPersona",
            "idPuesto__idDepartamento"
        ).order_by(
            "idPuesto__idDepartamento",
            "idPersona__Nombre_Completo"
        ),
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "idEmpleado"
            }
        ),
        label="Empleado"
    )

    class Meta:
        model = Onboarding
        fields = [
            "idEmpleado",
            "idDepartamento",
            "Fecha_Inicio"
        ]

        widgets = {
            "idDepartamento": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "idDepartamento"
                }
            ),
            "Fecha_Inicio": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            )
        }

        labels = {
            "idDepartamento": "Departamento",
            "Fecha_Inicio": "Fecha de Inicio"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Carga del listado base de todos los departamentos
        self.fields["idDepartamento"].queryset = Departamento.objects.all()

        # Filtrado dinámico en modo Edición (si la instancia ya existe en BD)
        if self.instance and self.instance.pk:
            empleado = self.instance.idEmpleado

            if empleado and empleado.idPuesto:
                departamento = empleado.idPuesto.idDepartamento

                # Restringe la lista de empleados únicamente a los de su mismo departamento
                self.fields["idEmpleado"].queryset = (
                    Empleado.objects.select_related(
                        "idPersona",
                        "idPuesto__idDepartamento"
                    )
                    .filter(
                        idPuesto__idDepartamento=departamento
                    )
                    .order_by(
                        "idPersona__Nombre_Completo"
                    )
                )



# =========================================================
# FORMULARIO: Detalle de Actividad de Onboarding
# =========================================================
class OnboardingActividadForm(forms.ModelForm):
    """
    Formulario basado en el modelo OnboardingActividad.
    
    Gestiona el registro y la edición del detalle de las actividades 
    de incorporación (onboarding), personalizando el renderizado 
    de los campos con clases de Bootstrap y etiquetas descriptivas.
    """

    class Meta:
        # Modelo de Django asociado a este formulario
        model = OnboardingActividad

        # Campos del modelo que se incluirán e interactuarán en la vista/HTML
        fields = [
            "idActividad",
            "id_Estatus_Vacante",
            "Fecha_Programada",
            "Fecha_Realizada",
            "Observaciones"
        ]

        # Configuración de los componentes visuales (HTML widgets) y sus atributos CSS/HTML
        widgets = {
            # Selector desplegable para la actividad asociada
            "idActividad": forms.Select(
                attrs={
                    "class": "form-select"  # Clase Bootstrap 5 para menús desplegables
                }
            ),

            # Selector desplegable para definir el estado actual del proceso/vacante
            "id_Estatus_Vacante": forms.Select(
                attrs={
                    "class": "form-select"  # Clase Bootstrap 5 para menús desplegables
                }
            ),

            # Selector de fecha nativo del navegador para la programación de la actividad
            "Fecha_Programada": forms.DateInput(
                attrs={
                    "type": "date",          # Fuerza el input nativo HTML5 con calendario (<input type="date">)
                    "class": "form-control"   # Estilo estándar de Bootstrap para inputs
                }
            ),

            # Selector de fecha nativo del navegador para cuando la actividad fue realizada
            "Fecha_Realizada": forms.DateInput(
                attrs={
                    "type": "date",          # Fuerza el input nativo HTML5 con calendario (<input type="date">)
                    "class": "form-control"   # Estilo estándar de Bootstrap para inputs
                }
            ),

            # Área de texto multilínea para añadir notas o comentarios de la actividad
            "Observaciones": forms.Textarea(
                attrs={
                    "class": "form-control", # Estilo estándar de Bootstrap para campos de texto
                    "rows": 3                 # Define la altura inicial visible (3 líneas de texto)
                }
            )
        }

        # Etiquetas legibles para los campos que se renderizan dentro de las etiquetas <label>
        labels = {
            "idActividad": "Actividad",
            "id_Estatus_Vacante": "Estado",
            "Fecha_Programada": "Fecha Programada",
            "Fecha_Realizada": "Fecha Realizada",
            "Observaciones": "Observaciones"
        }



# =========================================================
# FORMULARIO: Offboarding (Desvinculación de Empleados)
# =========================================================
class OffboardingForm(forms.ModelForm):
    """
    Formulario basado en el modelo Offboarding.
    
    Permite registrar la salida o baja de un empleado, optimizando 
    las consultas a la base de datos (ORM) para el listado de personal 
    y agrupando dinámicamente las causas de baja en el menú desplegable.
    """

    class Meta:
        # Modelo principal asociado al formulario
        model = Offboarding

        # Campos que serán editables y procesados por el formulario
        fields = [
            "idEmpleado",
            "idCausa",
            "Fecha_Salida",
            "Descrip_Causa"
        ]

        # Personalización de widgets HTML (estilos Bootstrap e IDs nativos)
        widgets = {
            # Desplegable para seleccionar al empleado
            "idEmpleado": forms.Select(
                attrs={
                    "class": "form-select", # Estilo Bootstrap 5 para <select>
                    "id": "idEmpleado"     # ID explícito para manipulaciones en JavaScript si se requiere
                }
            ),

            # Desplegable para seleccionar el tipo o categoría de causa de salida
            "idCausa": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "idCausa"
                }
            ),

            # Campo de fecha con selector interactivo del navegador
            "Fecha_Salida": forms.DateInput(
                attrs={
                    "type": "date",        # Fuerza el renderizado de <input type="date"> con calendario
                    "class": "form-control" # Estilo estándar de Bootstrap para inputs de texto/fecha
                }
            ),

            # Campo de texto multilínea para detallar los motivos
            "Descrip_Causa": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,              # Define una altura inicial de 3 filas visibles
                    "placeholder": "Describa brevemente el motivo de la salida..." # Texto guía
                }
            )
        }

        # Nombres visibles para las etiquetas (<label>) en el HTML
        labels = {
            "idEmpleado": "Empleado",
            "idCausa": "Causa de Salida",
            "Fecha_Salida": "Fecha de Salida",
            "Descrip_Causa": "Descripción de la Causa"
        }

    def __init__(self, *args, **kwargs):
        """
        Constructor personalizado para inicializar y personalizar los QuerySets 
        y las opciones (`choices`) de los campos desplegables en tiempo de ejecución.
        """
        super().__init__(*args, **kwargs)

        # =====================================================
        # EMPLEADOS: Optimización y Ordenamiento
        # =====================================================
        # 'select_related' realiza un JOIN en la BD para traer la información de 'idPersona'
        # en una sola consulta SQL (evitando el problema de la consulta N+1).
        self.fields["idEmpleado"].queryset = Empleado.objects.select_related(
            "idPersona"
        ).order_by(
            "idPersona__Nombre_Completo" # Ordena alfabéticamente por el nombre del empleado
        )
        
        # Define el texto para la opción vacía inicial del <select>
        self.fields["idEmpleado"].empty_label = "Seleccionar empleado..."

        # =====================================================
        # CAUSAS DE SALIDA: Agrupación con <optgroup> HTML
        # =====================================================
        # Obtiene todas las causas ordenadas secuencialmente por Categoría y Causa
        self.fields["idCausa"].queryset = CausaSalida.objects.order_by(
            "Categoria",
            "Causa"
        )

        # Establece la opción por defecto cuando no se ha seleccionado nada
        self.fields["idCausa"].choices = [
            ("", "Seleccione la causa legal...")
        ]

        # Diccionario auxiliar para construir la estructura de grupos de opciones
        categorias = {}

        # Recorre cada objeto de CausaSalida devuelto por el queryset
        for causa in self.fields["idCausa"].queryset:
            # setdefault crea la clave del grupo si no existe y añade la tupla (VALOR, TEXTO)
            categorias.setdefault(
                causa.Categoria,
                []
            ).append(
                (
                    causa.idCausa, # Valor enviado al servidor (ID)
                    causa.Causa    # Texto visible en la interfaz
                )
            )

        # Transforma el diccionario a la estructura que Django traduce como <optgroup> en HTML:
        # [ ('Nombre_Categoria', [(id1, 'Causa1'), (id2, 'Causa2')]), ... ]
        self.fields["idCausa"].choices += [
            (
                categoria,
                opciones
            )
            for categoria, opciones in categorias.items()
        ]
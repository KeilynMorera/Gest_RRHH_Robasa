from django import forms
from .models import PremioAsignado
from itertools import groupby

from .models import *

class AccionPersonalForm(forms.ModelForm):
    class Meta:
        model = AccionPersonal
        fields = ['idEmpleado', 'Fecha']
        widgets = {
            'idEmpleado': forms.Select(attrs={'class': 'form-control', 'id': 'idEmpleado'}),
            'Fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'Fecha'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reemplazamos las etiquetas del select por el Nombre_Completo de la Persona enlazada
        self.fields['idEmpleado'].queryset = Empleado.objects.select_related('idPersona').all()
        self.fields['idEmpleado'].label_from_instance = lambda obj: f"{obj.idPersona.Nombre_Completo}"



class PremioForm(forms.ModelForm):
    class Meta:
        model = Premio
        fields = ['Descripcion', 'Alcance', 'Monto', 'id_KPI_Categoria', 'idCuadrante_9box_Perfil']
        labels = {
            'Descripcion': 'Descripción del Premio',
            'Alcance': 'Alcance',
            'Monto': 'Monto Monetario',
            'id_KPI_Categoria': 'Categoría de KPI',
            'idCuadrante_9box_Perfil': 'Perfil Cuadrante 9-Box',
        }
        widgets = {
            'Descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Premio al Vendedor del Mes'}),
            'Alcance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Departamental, Regional...'}),
            'Monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'id_KPI_Categoria': forms.Select(attrs={'class': 'form-control'}),
            'idCuadrante_9box_Perfil': forms.Select(attrs={'class': 'form-control'}),
        }



# =========================================================
# FORMULARIO: PREMIO ASIGNADO
# =========================================================

from django import forms

from .models import (
    PremioAsignado,
    Premio,
    KpiCabecera
)


class PremioAsignadoForm(forms.ModelForm):

    class Meta:

        model = PremioAsignado

        # =================================================
        # CAMPOS QUE EL USUARIO PUEDE INGRESAR/SELECCIONAR
        # =================================================

        fields = [
            'id_KPI',
            'idPremio',
            'Fecha_Registro',
        ]


        # =================================================
        # WIDGETS
        # =================================================

        widgets = {

            # =============================================
            # SELECCIÓN DEL KPI
            # =============================================

            'id_KPI': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'id_KPI'
                }
            ),


            # =============================================
            # SELECCIÓN DEL PREMIO
            # =============================================

            'idPremio': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'idPremio'
                }
            ),


            # =============================================
            # FECHA DE REGISTRO
            # =============================================

            'Fecha_Registro': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'id': 'id_Fecha_Registro'
                }
            ),

        }


    # =====================================================
    # INICIALIZACIÓN DEL FORMULARIO
    # =====================================================

    def __init__(self, *args, **kwargs):

        super().__init__(
            *args,
            **kwargs
        )


        # =================================================
        # LISTA DE KPI
        # =================================================
        #
        # Se muestran los KPI registrados.
        #
        # Se utiliza select_related para poder acceder
        # directamente a los datos del empleado y persona.
        #
        # =================================================

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


        # =================================================
        # LISTA DE PREMIOS
        # =================================================
        #
        # Se muestran los premios disponibles.
        #
        # También se obtiene la categoría relacionada
        # para facilitar la lógica posterior.
        #
        # =================================================

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


        # =================================================
        # TEXTOS DE AYUDA / ETIQUETAS
        # =================================================

        self.fields['id_KPI'].label = (
            'Registro KPI Evaluado'
        )

        self.fields['idPremio'].label = (
            'Premio Asociado'
        )

        self.fields['Fecha_Registro'].label = (
            'Fecha de Registro'
        )


        # =================================================
        # CAMPOS OBLIGATORIOS
        # =================================================

        self.fields['id_KPI'].required = True

        self.fields['idPremio'].required = True

        self.fields['Fecha_Registro'].required = True


# =========================================================
# CAMPO PERSONALIZADO: Empleado con Departamento visible
# =========================================================
class EmpleadoConDepartamentoField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return (
            f"{obj.idPersona.Nombre_Completo} "
            f"— {obj.idPuesto.idDepartamento.Nombre}"
        )


# =========================================================
# FORMULARIO: Onboarding
# =========================================================
class OnboardingForm(forms.ModelForm):

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

        self.fields["idDepartamento"].queryset = Departamento.objects.all()



# =========================================================
# FORMULARIO: Onboarding
# =========================================================
class OnboardingForm(forms.ModelForm):

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


    # =====================================================
    # AQUÍ VA EL NUEVO __init__
    # =====================================================
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["idDepartamento"].queryset = Departamento.objects.all()


        # Cuando se modifica una cabecera existente
        if self.instance and self.instance.pk:

            empleado = self.instance.idEmpleado

            if empleado and empleado.idPuesto:

                departamento = empleado.idPuesto.idDepartamento


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

    class Meta:
        model = OnboardingActividad

        fields = [
            "idActividad",
            "id_Estatus_Vacante",
            "Fecha_Programada",
            "Fecha_Realizada",
            "Observaciones"
        ]

        widgets = {
            "idActividad": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "id_Estatus_Vacante": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "Fecha_Programada": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "Fecha_Realizada": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "Observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            )
        }

        labels = {
            "idActividad": "Actividad",
            "id_Estatus_Vacante": "Estado",
            "Fecha_Programada": "Fecha Programada",
            "Fecha_Realizada": "Fecha Realizada",
            "Observaciones": "Observaciones"
        }



# =========================================================
# FORMULARIO: Offboarding
# =========================================================
class OffboardingForm(forms.ModelForm):

    class Meta:

        model = Offboarding

        fields = [
            "idEmpleado",
            "idCausa",
            "Fecha_Salida",
            "Descrip_Causa"
        ]

        widgets = {

            "idEmpleado": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "idEmpleado"
                }
            ),

            "idCausa": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "idCausa"
                }
            ),

            "Fecha_Salida": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "Descrip_Causa": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Describa brevemente el motivo de la salida..."
                }
            )

        }

        labels = {

            "idEmpleado": "Empleado",

            "idCausa": "Causa de Salida",

            "Fecha_Salida": "Fecha de Salida",

            "Descrip_Causa": "Descripción de la Causa"

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # =====================================================
        # EMPLEADOS
        # =====================================================
        self.fields["idEmpleado"].queryset = Empleado.objects.select_related(
            "idPersona"
        ).order_by(
            "idPersona__Nombre_Completo"
        )

        # =====================================================
        # CAUSAS DE SALIDA
        # =====================================================
        self.fields["idCausa"].queryset = CausaSalida.objects.order_by(
            "Categoria",
            "Causa"
        )

        # Agrupar las causas por categoría
        self.fields["idCausa"].choices = [
            ("", "Seleccione la causa legal...")
        ]

        categorias = {}

        for causa in self.fields["idCausa"].queryset:

            categorias.setdefault(
                causa.Categoria,
                []
            ).append(
                (
                    causa.idCausa,
                    causa.Causa
                )
            )

        self.fields["idCausa"].choices += [
            (
                categoria,
                opciones
            )
            for categoria, opciones in categorias.items()
        ]

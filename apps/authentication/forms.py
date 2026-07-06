from django import forms
from .models import AccionPersonal, Empleado
from .models import Premio, KpiCategoria, Cuadrante9BoxPerfil
from .models import Onboarding
from .models import PremioAsignado

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



from django import forms
from django.utils import timezone

from .models import (
    PremioAsignado,
    Premio,
    Empleado,
    KpiCabecera,
)


class PremioAsignadoForm(forms.ModelForm):

    # Campo auxiliar (no pertenece al modelo)
    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.filter(Activo=True).select_related("idPersona"),
        required=False,
        label="Empleado",
        widget=forms.Select(attrs={
            "class": "form-control",
            "id": "idEmpleado"
        })
    )

    class Meta:
        model = PremioAsignado

        fields = [
            "empleado",
            "id_KPI",
            "idPremio",
            "Monto_Liquidado",
            "Fecha_Registro",
        ]

        widgets = {

            "id_KPI": forms.Select(attrs={
                "class": "form-control",
                "id": "id_KPI",
            }),

            "idPremio": forms.Select(attrs={
                "class": "form-control",
                "id": "idPremio",
            }),

            "Monto_Liquidado": forms.NumberInput(attrs={
                "class": "form-control",
                "id": "Monto_Liquidado",
                "readonly": True,
            }),

            "Fecha_Registro": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fecha actual por defecto
        if not self.instance.pk:
            self.fields["Fecha_Registro"].initial = timezone.now().date()

        # Inicialmente el combo de KPI queda vacío.
        # Luego el JavaScript lo llena cuando se selecciona un empleado.
        self.fields["id_KPI"].queryset = KpiCabecera.objects.none()

        self.fields["idPremio"].queryset = Premio.objects.all().order_by("Descripcion")



# =========================================================
# FORMULARIO: Onboarding
# =========================================================
class OnboardingForm(forms.ModelForm):

    class Meta:

        model = Onboarding

        fields = [
            "idEmpleado",
            "idDepartamento",
            "Fecha_Inicio"
        ]

        widgets = {

            "idEmpleado": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "idEmpleado"
                }
            ),

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

            "idEmpleado": "Empleado",

            "idDepartamento": "Departamento",

            "Fecha_Inicio": "Fecha de Inicio"

        }

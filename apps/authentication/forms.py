from django import forms
from .models import AccionPersonal, Empleado
from .models import Premio, KpiCategoria, Cuadrante9BoxPerfil

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
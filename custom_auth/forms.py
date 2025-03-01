from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Area
from .models import EspacioFisico, SolicitudEspacio

class AreaCreationForm(forms.ModelForm):
    # Definimos el widget para el campo password
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Area
        fields = ['area', 'responsable', 'extension', 'password']
        # Usamos 'widgets' para agregar configuraciones personalizadas a los campos
        widgets = {
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'extension': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Área",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ingrese su Área'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ingrese su contraseña', 'id': 'password-field'})
    )

class EspacioFisicoForm(forms.ModelForm):
    class Meta:
        model = EspacioFisico
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del espacio'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese una descripción'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SolicitudEspacioForm(forms.ModelForm):
    class Meta:
        model = SolicitudEspacio
        fields = [
            'folio', 'area', 'responsable', 'extension', 'nombre',
            'espacio_prestamo', 'fecha', 'hora_inicio', 'hora_fin',
            'otras_especificaciones', 'tipo_actividad',
            'requiere_costo', 'costo', 'con_cargo_a', 'estado'
        ]

        widgets = {
            'folio': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),

            'area': forms.Select(attrs={'class': 'form-select', 'readonly': 'readonly'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'extension': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'espacio_prestamo': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},format='%Y-%m-%d'),

            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'otras_especificaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_actividad': forms.TextInput(attrs={'class': 'form-control'}),
            'requiere_costo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control'}),
            'con_cargo_a': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.HiddenInput(),  # Se oculta si no se quiere que el usuario lo edite
        }
        exclude = ['fecha_solicitud']
        exclude = ['estado']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['responsable'].initial = user.responsable
            self.fields['extension'].initial = user.extension
            self.fields['area'].initial = user

            self.fields['area'].disabled = True  # Deshabilitar el campo para que no sea editable

            self.fields['folio'].initial = self.generate_folio()
            self.fields['folio'].disabled = True  # Deshabilitar el campo para que no sea editable

    def generate_folio(self):
        last_folio = SolicitudEspacio.objects.order_by('id').last()
        if last_folio:
            num = int(last_folio.folio.split('-')[-1]) + 1
        else:
            num = 1
        return f"ED-{num:04d}"

    def clean(self):
        cleaned_data = super().clean()
        espacio_prestamo = cleaned_data.get('espacio_prestamo')
        fecha = cleaned_data.get('fecha')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        # Validar que hora_fin sea mayor que hora_inicio
        if hora_inicio and hora_fin and hora_fin <= hora_inicio:
            raise forms.ValidationError('La hora de fin debe ser mayor que la hora de inicio.')

        # Validar que no haya traslape en el uso del espacio
        if espacio_prestamo and fecha and hora_inicio and hora_fin:
            conflictos = SolicitudEspacio.objects.filter(
                espacio_prestamo=espacio_prestamo,
                fecha=fecha,
                hora_inicio__lt=hora_fin,  # Hora inicio existente antes del fin solicitado
                hora_fin__gt=hora_inicio   # Hora fin existente después del inicio solicitado
            ).exclude(id=self.instance.id)  # Excluir la misma solicitud si es edición

            if conflictos.exists():
                raise forms.ValidationError('El espacio ya está reservado en este horario. Elige un horario diferente.')

        return cleaned_data

#--------------------------------------------------------AGREGADOS PARA VER USUARIOS 24/02/25#

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['area', 'responsable', 'extension', 'is_active']
        labels = {
            'area': 'Área',
            'responsable': 'Responsable',
            'extension': 'Extensión',
            'is_active': 'Activo',
        }
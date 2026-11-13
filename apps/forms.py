from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from .models import Categoria, Laboratorio, Cliente, Medico, Medicamento, RecetaMedica, Venta


class FormularioBase(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            if isinstance(campo.widget, forms.DateInput):
                campo.widget.input_type = 'date'
            if isinstance(campo.widget, forms.DateTimeInput):
                campo.widget.input_type = 'datetime-local'
            if isinstance(campo.widget, forms.TimeInput):
                campo.widget.input_type = 'time'
            campo.widget.attrs.setdefault('class', 'campo')


class CategoriaForm(FormularioBase):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción del uso terapéutico o grupo farmacológico'}),
        }


class LaboratorioForm(FormularioBase):
    class Meta:
        model = Laboratorio
        fields = ['nombre', 'ruc', 'telefono', 'email', 'direccion', 'activo']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Dirección física o sede fiscal'}),
        }


class ClienteForm(FormularioBase):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'dni', 'telefono', 'email', 'direccion', 'alergias']
        widgets = {
            'alergias': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Alergias a fármacos o condiciones de salud'}),
            'direccion': forms.Textarea(attrs={'rows': 2}),
        }


class MedicoForm(FormularioBase):
    class Meta:
        model = Medico
        fields = ['nombre', 'apellido', 'colegiatura', 'especialidad', 'telefono', 'clinica_hospital', 'activo']


class MedicamentoForm(FormularioBase):
    class Meta:
        model = Medicamento
        fields = [
            'codigo_barras', 'nombre', 'principio_activo', 'categoria', 'laboratorio',
            'presentacion', 'concentracion', 'precio_compra', 'precio_venta',
            'stock', 'stock_minimo', 'lote', 'fecha_vencimiento', 'requiere_receta',
            'instrucciones', 'activo'
        ]
        widgets = {
            'fecha_vencimiento': forms.DateInput(format='%Y-%m-%d'),
            'instrucciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Condiciones de conservación (ej: mantener refrigerado entre 2°C y 8°C)'}),
        }


class RecetaMedicaForm(FormularioBase):
    class Meta:
        model = RecetaMedica
        fields = [
            'numero_receta', 'cliente', 'medico', 'medicamento', 'dosis',
            'frecuencia', 'duracion', 'diagnostico', 'indicaciones',
            'fecha_emision', 'fecha_vencimiento', 'estado'
        ]
        widgets = {
            'fecha_emision': forms.DateInput(format='%Y-%m-%d'),
            'fecha_vencimiento': forms.DateInput(format='%Y-%m-%d'),
            'indicaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Indicaciones de administración'}),
        }


class VentaForm(FormularioBase):
    class Meta:
        model = Venta
        fields = [
            'numero_comprobante', 'tipo_comprobante', 'cliente', 'medicamento',
            'cantidad', 'precio_unitario', 'total', 'metodo_pago', 'usuario',
            'fecha', 'estado', 'observaciones'
        ]
        widgets = {
            'fecha': forms.DateTimeInput(format='%Y-%m-%dT%H:%M'),
            'observaciones': forms.Textarea(attrs={'rows': 2, 'placeholder': 'N.° de operación o notas'}),
        }


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico corporativo')
    codigo = forms.CharField(
        label='Código de invitación (solo en producción)',
        required=False,
        widget=forms.PasswordInput,
        help_text='En desarrollo se puede dejar vacío; en producción es obligatorio.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email

    def clean_codigo(self):
        from django.utils.crypto import constant_time_compare
        codigo = self.cleaned_data.get('codigo', '')
        if not settings.DEBUG and not constant_time_compare(codigo, settings.REGISTRATION_CODE):
            raise forms.ValidationError('Código de invitación no válido.')
        return codigo

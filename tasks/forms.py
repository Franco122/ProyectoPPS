# tasks/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto, IngresoEfectivo, Proveedor

# Formulario para proveedores
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'empresa', 'telefono', 'email', 'direccion']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'cantidad', 'precio', 'marca']


class RegistroUsuarioForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        label='Nombre de usuario',
        help_text='Máximo 30 caracteres. Solo letras, números y @/./+/-/_'
    )
    email = forms.EmailField(label='Correo electrónico')

    password1 = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput,
        help_text='Debe tener al menos 8 caracteres, no ser común ni solo numérica.',
        error_messages={
            'La contraseña demasiado corta': 'La contraseña debe tener al menos 8 caracteres.',
            'La contraseña demasiado comun': 'La contraseña es demasiado común.',
            'La contraseña no pueden ser solo numeros': 'La contraseña no puede ser solo números.',
        }
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput,
        strip=False,
        help_text='Ingresá la misma contraseña para confirmar.',
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class IngresoEfectivoForm(forms.ModelForm):
    class Meta:
        model = IngresoEfectivo
        fields = ['monto', 'descripcion']
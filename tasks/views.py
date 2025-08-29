from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm, ProductoForm
from .models import Producto
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import IngresoEfectivo
from .forms import IngresoEfectivoForm
from django.db import models

# -------- Vistas públicas --------

# Registro
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("✅ Usuario creado:", user.username)  # Debug en consola
            messages.success(request, 'Usuario creado correctamente. Ahora podés iniciar sesión.')
            return redirect('login')
        else:
            print("❌ Errores del formulario:", form.errors)  # Debug en consola
            messages.error(request, 'Error al registrar. Verificá los datos.')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'register.html', {'form': form})



def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado con éxito. Ya podés iniciar sesión.')
            return redirect('login')  # Cambia 'login' por el nombre de tu URL de login
        else:
            messages.error(request, 'Por favor corregí los errores en el formulario.')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})
# Login
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'login.html')

# Logout
def logout_usuario(request):
    logout(request)
    return redirect('login')

# -------- Vistas privadas (requieren login) --------

@login_required
def inicio(request):
    if request.method == 'POST':
        form = IngresoEfectivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Asegurate de que la URL se llame 'inicio'
    else:
        form = IngresoEfectivoForm()

    ingresos = IngresoEfectivo.objects.order_by('-fecha')
    total_efectivo = sum(ing.monto for ing in ingresos)

    return render(request, 'inicio.html', {
        'form': form,
        'ingresos': ingresos,
        'total_efectivo': total_efectivo,
    })

@login_required
def bienvenida(request):
    return render(request, 'bienvenida.html', {'usuario': request.user})

@login_required
def inventario(request):
    return render(request, 'inventario.html')

@login_required
def proveedores(request):
    return render(request, 'proveedores.html')  

@login_required
def transacciones(request):
    return render(request, 'transacciones.html') 

@login_required
@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre'].strip().lower()
            categoria = form.cleaned_data['categoria'].strip().lower()
            cantidad = form.cleaned_data['cantidad']
            precio = form.cleaned_data['precio']
            stock = form.cleaned_data['stock']

            producto_existente = Producto.objects.filter(nombre=nombre, categoria=categoria).first()

            if producto_existente:
                # Si ya existe, actualizamos stock y cantidad
                producto_existente.cantidad += cantidad
                producto_existente.stock += stock
                producto_existente.precio = precio  
                producto_existente.save()
            else:
                form.save()

            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'agregar_producto.html', {'form': form})

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})


def agregar_efectivo(request):
    if request.method == 'POST':
        monto = request.POST['monto']
        descripcion = request.POST['descripcion']
        IngresoEfectivo.objects.create(monto=monto, descripcion=descripcion)
    return redirect('inicio')



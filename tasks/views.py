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
from django.shortcuts import get_object_or_404
from .models import IngresoEfectivo, IngresoVirtual, Egreso, CierreDiario
from datetime import datetime
from django.db.models import Sum


# Registro
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("✅ Usuario creado:", user.username)  
            messages.success(request, 'Usuario creado correctamente. Ahora podés iniciar sesión.')
            return redirect('login')
        else:
            print("❌ Errores del formulario:", form.errors) 
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
            return redirect('login')  
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
            return redirect('inicio') 
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
    ingresos = IngresoEfectivo.objects.all().order_by('-fecha')
    egresos = Egreso.objects.all().order_by('-fecha')
    cierres = CierreDiario.objects.all().order_by('-fecha')

    transacciones = []
    for ing in ingresos:
        transacciones.append({
            'descripcion': ing.descripcion,
            'categoria': 'Ingreso Efectivo',
            'monto': ing.monto,
            'fecha': ing.fecha
        })
    for eg in egresos:
        transacciones.append({
            'descripcion': eg.descripcion,
            'categoria': 'Egreso',
            'monto': eg.monto,
            'fecha': eg.fecha
        })
    # Sort by fecha descending
    transacciones.sort(key=lambda x: x['fecha'], reverse=True)

    return render(request, 'transacciones.html', {
        'transacciones': transacciones,
        'cierres': cierres
    })

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
            marca = form.cleaned_data['marca']

            producto_existente = Producto.objects.filter(nombre=nombre, categoria=categoria).first()

            if producto_existente:
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


@login_required
def eliminar_ingreso(request, pk):
    ingreso = get_object_or_404(IngresoEfectivo, pk=pk)
    ingreso.delete()
    return redirect('inicio')

@login_required
def editar_ingreso(request, pk):
    ingreso = get_object_or_404(IngresoEfectivo, pk=pk)
    if request.method == "POST":
        form = IngresoEfectivoForm(request.POST, instance=ingreso)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = IngresoEfectivoForm(instance=ingreso)
    return render(request, 'editar_ingreso.html', {'form': form})


def cerrar_dia(request):
    if request.method == "POST":
        hoy = datetime.now().date()
        ingresos = IngresoEfectivo.objects.filter(fecha__date=hoy).aggregate(total=Sum('monto'))['total'] or 0
        egresos = Egreso.objects.filter(fecha__date=hoy).aggregate(total=Sum('monto'))['total'] or 0
        total_final = ingresos - egresos

        CierreDiario.objects.create(
            fecha=hoy,
            monto_ingresos=ingresos,
            monto_egresos=egresos,
            monto_total=total_final
        )

       
        return redirect('inicio')
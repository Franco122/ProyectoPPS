
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import models, transaction
from django.db.models import Sum
from datetime import datetime
from .forms import RegistroUsuarioForm, ProductoForm, IngresoEfectivoForm, ProveedorForm, IngresoVirtualForm, GastoForm
from .models import Producto, IngresoEfectivo, IngresoVirtual, Egreso, CierreDiario, Proveedor, Gasto

# Vista para editar movimiento virtual
@login_required
def editar_virtual(request, pk):
    ingreso = get_object_or_404(IngresoVirtual, pk=pk)
    if request.method == 'POST':
        form = IngresoVirtualForm(request.POST, instance=ingreso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimiento virtual editado correctamente.')
            return redirect('inicio')
    else:
        form = IngresoVirtualForm(instance=ingreso)
    return render(request, 'agregar_virtual.html', {'form': form, 'editar': True, 'ingreso': ingreso})

# Vista para eliminar movimiento virtual
@login_required
def eliminar_virtual(request, pk):
    ingreso = get_object_or_404(IngresoVirtual, pk=pk)
    if request.method == 'POST':
        ingreso.delete()
        messages.success(request, 'Movimiento virtual eliminado correctamente.')
        return redirect('inicio')
    return render(request, 'eliminar_virtual.html', {'ingreso': ingreso})

# Vista para agregar movimiento virtual
@login_required
def agregar_virtual(request):
    if request.method == 'POST':
        form = IngresoVirtualForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimiento virtual agregado correctamente.')
            return redirect('inicio')
    else:
        form = IngresoVirtualForm()
    return render(request, 'agregar_virtual.html', {'form': form, 'editar': False})

# Vista para eliminar proveedor
@login_required
def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado correctamente.')
        return redirect('proveedores')
    return render(request, 'eliminar_proveedor.html', {'proveedor': proveedor})

# Vista para editar proveedor
@login_required
def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor editado correctamente.')
            return redirect('proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'agregar_proveedor.html', {'form': form, 'editar': True, 'proveedor': proveedor})

# Vista para sumar stock
@login_required
def sumar_stock(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.cantidad += 1
    producto.save()
    messages.success(request, f'Se sumó 1 a la cantidad de {producto.nombre}.')
    return redirect('inventario')

# Vista para eliminar producto
@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('inventario')
    return render(request, 'eliminar_producto.html', {'producto': producto})

# Vista para editar producto
@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto editado correctamente.')
            return redirect('inventario')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'agregar_producto.html', {'form': form, 'editar': True, 'producto': producto})

# --- Vistas ---

@login_required
def agregar_proveedor(request):
    from .forms import ProveedorForm
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor agregado correctamente.')
            return redirect('proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'agregar_proveedor.html', {'form': form, 'editar': False})


# Registro
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("✅ Usuario creado:", user.username)  
            # Quita este mensaje:
            # messages.success(request, 'Usuario creado correctamente. Ahora podés iniciar sesión.')
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
            # Quita este mensaje:
            # messages.success(request, 'Usuario registrado con éxito. Ya podés iniciar sesión.')
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
    # Limpia los mensajes acumulados antes de renderizar el login
    storage = messages.get_messages(request)
    for _ in storage:
        pass
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
    ingresos_virtuales = IngresoVirtual.objects.order_by('-fecha')
    total_virtual = sum(getattr(ing, 'monto', 0) for ing in ingresos_virtuales)

    gastos = Gasto.objects.order_by('-fecha')
    suma_gastos = gastos.aggregate(total=models.Sum('monto'))['total'] or 0

    return render(request, 'inicio.html', {
        'form': form,
        'ingresos': ingresos,
        'total_efectivo': total_efectivo,
        'ingresos_virtuales': ingresos_virtuales,
        'total_virtual': total_virtual,
        'gastos': gastos,
        'suma_gastos': suma_gastos,
        'productos_all': Producto.objects.all(),
    })
# Vista para agregar gastos
@login_required
def agregar_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gasto agregado correctamente.')
            return redirect('inicio')
    else:
        form = GastoForm()
    return render(request, 'agregar_gasto.html', {'form': form})

# Vista para editar gasto
@login_required
def editar_gasto(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk)
    if request.method == 'POST':
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gasto editado correctamente.')
            return redirect('inicio')
    else:
        form = GastoForm(instance=gasto)
    return render(request, 'agregar_gasto.html', {'form': form, 'editar': True, 'gasto': gasto})

# Vista para eliminar gasto
@login_required
def eliminar_gasto(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk)
    if request.method == 'POST':
        gasto.delete()
        messages.success(request, 'Gasto eliminado correctamente.')
        return redirect('inicio')
    return render(request, 'eliminar_gasto.html', {'gasto': gasto})

@login_required
def bienvenida(request):
    return render(request, 'bienvenida.html', {'usuario': request.user})

@login_required

def inventario(request):
    q = request.GET.get('q', '').strip()
    productos = Producto.objects.all()
    if q:
        productos = productos.filter(
            models.Q(nombre__icontains=q) |
            models.Q(categoria__icontains=q) |
            models.Q(marca__icontains=q)
        )
    return render(request, 'inventario.html', {'productos': productos})

@login_required
def proveedores(request):
    from .models import Proveedor
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores.html', {'proveedores': proveedores})

@login_required
def transacciones(request):
    ingresos = IngresoEfectivo.objects.all().order_by('-fecha')
    ingresos_virtuales = IngresoVirtual.objects.all().order_by('-fecha')
    egresos = Egreso.objects.all().order_by('-fecha')
    gastos = Gasto.objects.all().order_by('-fecha')
    cierres = CierreDiario.objects.all().order_by('-fecha')

    transacciones = []
    for ing in ingresos:
        transacciones.append({
            'descripcion': ing.descripcion,
            'categoria': 'Ingreso Efectivo',
            'monto': ing.monto,
            'fecha': ing.fecha
        })
    # incluir ingresos virtuales en el historial
    for ving in ingresos_virtuales:
        transacciones.append({
            'descripcion': ving.descripcion,
            'categoria': 'Ingreso Virtual',
            'monto': ving.monto,
            'fecha': ving.fecha
        })
    for eg in egresos:
        transacciones.append({
            'descripcion': eg.descripcion,
            'categoria': 'Egreso',
            'monto': eg.monto,
            'fecha': eg.fecha
        })
    # incluir gastos como egresos
    for gasto in gastos:
        transacciones.append({
            'descripcion': gasto.descripcion,
            'categoria': 'Egreso',
            'monto': gasto.monto,
            'fecha': gasto.fecha
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
            marca = form.cleaned_data['marca']

            producto_existente = Producto.objects.filter(nombre=nombre, categoria=categoria).first()

            if producto_existente:
                producto_existente.cantidad += cantidad
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


@login_required
def agregar_efectivo(request):
    # Maneja el formulario de ingreso en efectivo y opcionalmente descuenta producto del inventario
    if request.method == 'POST':
        form = IngresoEfectivoForm(request.POST)
        if form.is_valid():
            monto = form.cleaned_data['monto']
            descripcion = form.cleaned_data['descripcion']
            producto = form.cleaned_data.get('producto')
            cantidad_producto = form.cleaned_data.get('cantidad_producto')

            # Operación atómica: crear ingreso y descontar stock si corresponde
            try:
                with transaction.atomic():
                    if producto and cantidad_producto:
                        # Volver a obtener el producto con bloqueo para evitar condiciones de carrera
                        producto = Producto.objects.select_for_update().get(pk=producto.pk)
                        if producto.cantidad < cantidad_producto:
                            messages.error(request, f"Stock insuficiente para {producto.nombre}. Stock actual: {producto.cantidad}")
                            return redirect('inicio')
                        producto.cantidad -= cantidad_producto
                        producto.save()
                    IngresoEfectivo.objects.create(monto=monto, descripcion=descripcion)
                    messages.success(request, 'Ingreso en efectivo agregado correctamente.')
            except Exception as e:
                messages.error(request, 'Ocurrió un error al procesar el ingreso.')
        else:
            messages.error(request, 'Formulario de ingreso inválido. Verificá los datos.')
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
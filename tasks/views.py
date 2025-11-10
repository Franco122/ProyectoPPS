
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.db import models, transaction
from django.db.models import Sum
from datetime import datetime
from .forms import RegistroUsuarioForm, ProductoForm, IngresoEfectivoForm, ProveedorForm, IngresoVirtualForm, GastoForm
from .forms import VentaForm, VentaItemForm
from django.forms import inlineformset_factory
from .models import Producto, IngresoEfectivo, IngresoVirtual, Egreso, CierreDiario, Proveedor, Gasto, Venta, VentaItem

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
    # Maneja el formulario de ingreso virtual y opcionalmente descuenta producto del inventario
    if request.method == 'POST':
        form = IngresoVirtualForm(request.POST)
        if form.is_valid():
            monto = form.cleaned_data['monto']
            descripcion = form.cleaned_data['descripcion']
            producto = form.cleaned_data.get('producto')
            cantidad_producto = form.cleaned_data.get('cantidad_producto')

            try:
                with transaction.atomic():
                    # descripción general opcional (si el usuario la completó en la parte superior)
                    general_desc = (request.POST.get('descripcion_general') or '').strip()
                    if producto and cantidad_producto:
                        producto = Producto.objects.select_for_update().get(pk=producto.pk)
                        if producto.cantidad < cantidad_producto:
                            messages.error(request, f"Stock insuficiente para {producto.nombre}. Stock actual: {producto.cantidad}")
                            return redirect('inicio')
                        producto.cantidad -= cantidad_producto
                        producto.save()
                    IngresoVirtual.objects.create(
                        monto=monto, 
                        descripcion=descripcion,
                        producto=producto if producto else None,
                        cantidad_producto=cantidad_producto if producto else None
                    )
                    messages.success(request, 'Movimiento virtual agregado correctamente.')
            except Exception:
                messages.error(request, 'Ocurrió un error al procesar el ingreso virtual.')
        else:
            messages.error(request, 'Formulario de ingreso virtual inválido. Verificá los datos.')
        return redirect('inicio')
    else:
        form = IngresoVirtualForm()
    return render(request, 'agregar_virtual.html', {'form': form, 'editar': False})


@login_required
def movimientos_virtuales(request):
    """Página dedicada a movimientos virtuales: formulario y lista.
    Lógica copiada de la gestión de ingresos en efectivo / agregar_virtual,
    pero en una vista separada que muestra solo movimientos virtuales.
    """
    # Usar un formset para permitir múltiples productos en un solo envío
    from django.forms import modelformset_factory
    IngresoVirtualFormSet = modelformset_factory(IngresoVirtual, form=IngresoVirtualForm, extra=1, can_delete=True)

    if request.method == 'POST':
        formset = IngresoVirtualFormSet(request.POST, queryset=IngresoVirtual.objects.none(), prefix='vitems')
        if formset.is_valid():
            try:
                with transaction.atomic():
                    # descripción general opcional (si el usuario la completó en la parte superior)
                    general_desc = (request.POST.get('descripcion_general') or '').strip()
                    # procesar cada formulario válido (no marcado para DELETE)
                    for f in formset:
                        if not f.cleaned_data or f.cleaned_data.get('DELETE', False):
                            continue
                        producto = f.cleaned_data.get('producto')
                        cantidad_producto = f.cleaned_data.get('cantidad_producto')
                        monto = f.cleaned_data.get('monto')
                        descripcion = f.cleaned_data.get('descripcion')
                        # si hay una descripción general, la usamos en lugar de la descripción por línea
                        if general_desc:
                            descripcion = general_desc

                        if producto and cantidad_producto:
                            p = Producto.objects.select_for_update().get(pk=producto.pk)
                            if p.cantidad < cantidad_producto:
                                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                                    return JsonResponse({'success': False, 'message': f'Stock insuficiente para {producto.nombre}. Stock actual: {p.cantidad}'}, status=400)
                                messages.error(request, f"Stock insuficiente para {producto.nombre}. Stock actual: {p.cantidad}")
                                return redirect('movimientos_virtuales')
                            p.cantidad -= cantidad_producto
                            p.save()

                        # crear el ingreso virtual por cada línea
                        IngresoVirtual.objects.create(
                            monto=monto,
                            descripcion=descripcion,
                            producto=producto if producto else None,
                            cantidad_producto=cantidad_producto if producto else None
                        )

                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'Movimientos virtuales agregados correctamente'})
                messages.success(request, 'Movimientos virtuales agregados correctamente.')
                return redirect('movimientos_virtuales')
            except Exception as e:
                print('DEBUG: Exception in movimientos_virtuales:', e)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Ocurrió un error al procesar los ingresos virtuales.'}, status=500)
                messages.error(request, 'Ocurrió un error al procesar los ingresos virtuales.')
                return redirect('movimientos_virtuales')
        else:
            # formset inválido
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Formulario inválido', 'errors': formset.errors}, status=400)
            messages.error(request, 'Por favor corregí los errores en el formulario.')
            return redirect('movimientos_virtuales')
    else:
        formset = IngresoVirtualFormSet(queryset=IngresoVirtual.objects.none(), prefix='vitems')

    return render(request, 'movimientos_virtuales.html', {
        'formset': formset,
        'productos_all': Producto.objects.all(),
    })

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
        try:
            # Eliminar primero los VentaItem asociados
            VentaItem.objects.filter(producto=producto).delete()
            # Luego eliminar el producto
            producto.delete()
            messages.success(request, 'Producto eliminado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el producto: {str(e)}')
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
    # Calculamos monto a mostrar: si el ingreso tiene producto y cantidad_producto usamos
    
    ingresos = IngresoEfectivo.objects.order_by('-fecha')
    ingresos_display = []
    for ing in ingresos:
        try:
            if ing.producto and ing.cantidad_producto:
                monto_calc = (ing.producto.precio or 0) * (ing.cantidad_producto or 0)
            else:
                monto_calc = ing.monto
        except Exception:
            monto_calc = ing.monto
        ingresos_display.append({'obj': ing, 'monto_display': monto_calc})
    total_efectivo = sum(item['monto_display'] for item in ingresos_display)
    ingresos_virtuales = IngresoVirtual.objects.order_by('-fecha')
    ingresos_virtual_display = []
    for ving in ingresos_virtuales:
        try:
            if ving.producto and ving.cantidad_producto:
                monto_calc = (ving.producto.precio or 0) * (ving.cantidad_producto or 0)
                precio_unitario = ving.producto.precio
            else:
                monto_calc = ving.monto
        except Exception:
            monto_calc = ving.monto
            precio_unitario = None
        ingresos_virtual_display.append({'obj': ving, 'monto_display': monto_calc, 'precio_unitario': precio_unitario})
    total_virtual = sum(item['monto_display'] for item in ingresos_virtual_display)

    gastos = Gasto.objects.order_by('-fecha')
    suma_gastos = gastos.aggregate(total=models.Sum('monto'))['total'] or 0

    return render(request, 'inicio.html', {
        'form': form,
        'ingresos': ingresos_display,
        'total_efectivo': total_efectivo,
        'ingresos_virtuales': ingresos_virtual_display,
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
            models.Q(categoria__icontains=q)
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
        # Construir descripción combinada
        descripcion_completa = ing.descripcion or ""
        if ing.producto:
            if descripcion_completa:
                descripcion_completa = f"{ing.producto.nombre} x{ing.cantidad_producto} - {descripcion_completa}"
            else:
                descripcion_completa = f"{ing.producto.nombre} x{ing.cantidad_producto}"

        transacciones.append({
            'descripcion': descripcion_completa if descripcion_completa else "Sin descripción",
            'categoria': 'Ingreso Efectivo',
            'monto': ing.monto,
            'fecha': ing.fecha
        })
    # incluir ingresos virtuales en el historial
    for ving in ingresos_virtuales:
        # Construir descripción combinada
        descripcion_completa = ving.descripcion or ""
        if ving.producto:
            if descripcion_completa:
                descripcion_completa = f"{ving.producto.nombre} x{ving.cantidad_producto} - {descripcion_completa}"
            else:
                descripcion_completa = f"{ving.producto.nombre} x{ving.cantidad_producto}"

        transacciones.append({
            'descripcion': descripcion_completa if descripcion_completa else "Sin descripción",
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
                    IngresoEfectivo.objects.create(
                        monto=monto, 
                        descripcion=descripcion,
                        producto=producto if producto else None,
                        cantidad_producto=cantidad_producto if producto else None
                    )
                    messages.success(request, 'Ingreso en efectivo agregado correctamente.')
            except Exception as e:
                messages.error(request, 'Ocurrió un error al procesar el ingreso.')
        else:
            messages.error(request, 'Formulario de ingreso inválido. Verificá los datos.')
    return redirect('inicio')


@login_required
def agregar_venta(request):
    """Registrar una venta con múltiples productos en un formset.
    Resta stock de los productos y crea un registro de IngresoEfectivo con el total.
    """
    # crear formset en tiempo de ejecución para evitar import-time issues
    VentaItemFormSet = inlineformset_factory(Venta, VentaItem, form=VentaItemForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = VentaForm(request.POST)
        # usar una instancia temporal para validar inline formset
        venta_temp = Venta()
        formset = VentaItemFormSet(request.POST, instance=venta_temp, prefix='items')

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # recopilar ids de productos en el formset (no eliminados)
                    product_ids = []
                    for f in formset:
                        if not f.cleaned_data or f.cleaned_data.get('DELETE', False):
                            continue
                        product_ids.append(f.cleaned_data['producto'].pk)

                    productos = Producto.objects.select_for_update().filter(pk__in=product_ids)
                    prod_map = {p.pk: p for p in productos}

                    total = 0
                    items = []
                    for f in formset:
                        if not f.cleaned_data or f.cleaned_data.get('DELETE', False):
                            continue
                        producto = f.cleaned_data['producto']
                        cantidad = f.cleaned_data['cantidad']
                        precio_unitario = f.cleaned_data.get('precio_unitario') or producto.precio

                        p = prod_map.get(producto.pk)
                        if p is None:
                            messages.error(request, f"Producto {producto.nombre} no encontrado.")
                            return redirect('agregar_venta')
                        if p.cantidad < cantidad:
                            messages.error(request, f"Stock insuficiente para {producto.nombre}. Stock actual: {p.cantidad}")
                            return redirect('agregar_venta')

                        total += precio_unitario * cantidad
                        items.append((producto, cantidad, precio_unitario))

                    venta = Venta.objects.create(total=total, descripcion=form.cleaned_data.get('descripcion',''))
                    for producto, cantidad, precio_unitario in items:
                        VentaItem.objects.create(venta=venta, producto=producto, cantidad=cantidad, precio_unitario=precio_unitario)
                        p = prod_map[producto.pk]
                        p.cantidad -= cantidad
                        p.save()

                    # Crear registro de ingreso en efectivo ligado a la venta (opcional)
                    # Usar la descripción de la venta si está disponible, sino usar el número de venta
                    descripcion = venta.descripcion if venta.descripcion else f"Venta #{venta.id}"
                    IngresoEfectivo.objects.create(monto=total, descripcion=descripcion)

                    messages.success(request, 'Venta registrada correctamente.')
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'success': True, 'message': 'Venta registrada correctamente'})
                    return redirect('transacciones')
            except Exception as e:
                print('DEBUG: Exception in agregar_venta:', e)
                messages.error(request, 'Ocurrió un error al procesar la venta.')
        else:
            # debug prints para tests/local
            if not form.is_valid():
                print('DEBUG: VentaForm errors:', form.errors)
            if not formset.is_valid():
                print('DEBUG: VentaItem formset errors:', formset.errors)
            messages.error(request, 'Por favor corregí los errores en el formulario de venta.')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Por favor corregí los errores en el formulario de venta.',
                    'errors': {
                        'form': form.errors,
                        'formset': formset.errors
                    }
                })
    else:
        form = VentaForm()
        venta_temp = Venta()
        formset = VentaItemFormSet(instance=venta_temp, prefix='items')

    return render(request, 'agregar_venta.html', {'form': form, 'formset': formset, 'productos_all': Producto.objects.all()})


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

@login_required
def get_product_price(request, producto_id):
    try:
        producto = Producto.objects.get(pk=producto_id)
        return JsonResponse({'precio': producto.precio})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
       
        return redirect('inicio')
    # ...existing code...

from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', lambda request: redirect('login')),
    
    path('registro/', views.registrar_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    
    # Vistas protegidas (solo accesibles con login)
    path('inicio/', views.inicio, name='inicio'),
    path('inventario/', views.inventario, name='inventario'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/sumar-stock/<int:pk>/', views.sumar_stock, name='sumar_stock'),
    path('inventario/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('proveedores/', views.proveedores, name='proveedores'),
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/editar/<int:pk>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('transacciones/', views.transacciones, name='transacciones'),
    path('agregar-efectivo/', views.agregar_efectivo, name='agregar_efectivo'),
    path('agregar-virtual/', views.agregar_virtual, name='agregar_virtual'),
    path('movimientos/virtuales/', views.movimientos_virtuales, name='movimientos_virtuales'),
    path('ventas/agregar/', views.agregar_venta, name='agregar_venta'),
    path('ventas/', views.transacciones, name='ventas'),
    path('virtual/editar/<int:pk>/', views.editar_virtual, name='editar_virtual'),
    path('virtual/eliminar/<int:pk>/', views.eliminar_virtual, name='eliminar_virtual'),
    path('ingresos/editar/<int:pk>/', views.editar_ingreso, name='editar_ingreso'),
    path('ingresos/eliminar/<int:pk>/', views.eliminar_ingreso, name='eliminar_ingreso'),
    path("cerrar-dia/", views.cerrar_dia, name="cerrar_dia"),
    path('agregar-gasto/', views.agregar_gasto, name='agregar_gasto'),
    path('gastos/editar/<int:pk>/', views.editar_gasto, name='editar_gasto'),
    path('gastos/eliminar/<int:pk>/', views.eliminar_gasto, name='eliminar_gasto'),
    path('get_product_price/<int:producto_id>/', views.get_product_price, name='get_product_price'),
]
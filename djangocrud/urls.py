from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redirige '/' a '/login/' para mayor claridad
    path('', lambda request: redirect('login')),
    
    # Registro y login/logout
    path('registro/', views.registrar_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    
    # Vistas protegidas (solo accesibles con login)
    path('inicio/', views.inicio, name='inicio'),
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('proveedores/', views.proveedores, name='proveedores'),
    path('transacciones/', views.transacciones, name='transacciones'),
    path('agregar-efectivo/', views.agregar_efectivo, name='agregar_efectivo'),
]
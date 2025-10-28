from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Producto, IngresoEfectivo


class IngresoEfectivoStockTests(TestCase):
	def setUp(self):
		# Usuario para acceder a vistas protegidas
		self.user = User.objects.create_user(username='tester', password='pass')

	def test_descuento_stock_exitoso(self):
		self.client.login(username='tester', password='pass')
		producto = Producto.objects.create(nombre='manzana', categoria='fruta', cantidad=10, precio=1.00)

		data = {
			'monto': '100.00',
			'descripcion': 'Venta con descuento',
			'producto': str(producto.id),
			'cantidad_producto': '3'
		}

		resp = self.client.post(reverse('agregar_efectivo'), data)
		producto.refresh_from_db()

		self.assertEqual(producto.cantidad, 7)
		self.assertTrue(IngresoEfectivo.objects.filter(descripcion='Venta con descuento', monto='100.00').exists())

	def test_descuento_stock_insuficiente(self):
		self.client.login(username='tester', password='pass')
		producto = Producto.objects.create(nombre='pan', categoria='alimento', cantidad=2, precio=0.50)

		data = {
			'monto': '50.00',
			'descripcion': 'Venta fallo',
			'producto': str(producto.id),
			'cantidad_producto': '5'
		}

		resp = self.client.post(reverse('agregar_efectivo'), data)
		producto.refresh_from_db()

		# No se debió modificar el stock ni crear el ingreso
		self.assertEqual(producto.cantidad, 2)
		self.assertFalse(IngresoEfectivo.objects.filter(descripcion='Venta fallo').exists())

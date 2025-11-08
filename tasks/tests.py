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


class VentaMultiProductoTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='vendedor', password='pass')

	def test_venta_multiple_descuenta_stock_y_crea_venta(self):
		self.client.login(username='vendedor', password='pass')
		p1 = Producto.objects.create(nombre='leche', categoria='lacteos', cantidad=10, precio=2.00)
		p2 = Producto.objects.create(nombre='galletas', categoria='snack', cantidad=5, precio=1.50)

		# Construir POST para formset: usar indices 0 and 1
		data = {
			'descripcion': 'Venta test',
			'items-TOTAL_FORMS': '2',
			'items-INITIAL_FORMS': '0',
			'items-MIN_NUM_FORMS': '0',
			'items-MAX_NUM_FORMS': '1000',
			'items-0-producto': str(p1.id),
			'items-0-cantidad': '3',
			'items-0-precio_unitario': '',
			'items-1-producto': str(p2.id),
			'items-1-cantidad': '2',
			'items-1-precio_unitario': '',
		}

		resp = self.client.post(reverse('agregar_venta'), data)
		p1.refresh_from_db(); p2.refresh_from_db()

		self.assertEqual(p1.cantidad, 7)
		self.assertEqual(p2.cantidad, 3)
		# Venta e IngresoEfectivo creados
		from .models import Venta
		self.assertTrue(Venta.objects.filter(descripcion='Venta test').exists())
		self.assertTrue(IngresoEfectivo.objects.filter(descripcion__contains='Venta #').exists())

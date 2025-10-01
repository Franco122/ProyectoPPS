from django.db import models

# Modelo para proveedores
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)
    email = models.EmailField()
    direccion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.empresa})"

from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=100, default="Sin marca")

    def save(self, *args, **kwargs):
        # Normalizamos a minúsculas y sin espacios extra
        self.nombre = self.nombre.strip().lower()
        self.categoria = self.categoria.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
# models.py
class IngresoEfectivo(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.monto} - {self.descripcion}"
    

class IngresoVirtual(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha} - {self.monto}"

class CierreDiario(models.Model):
    fecha = models.DateField()
    monto_ingresos = models.DecimalField(max_digits=10, decimal_places=2)
    monto_egresos = models.DecimalField(max_digits=10, decimal_places=2)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)

class Egreso(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[Egreso] {self.fecha} - ${self.monto}"
    
class Gasto(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gasto: {self.monto} ({self.descripcion})"



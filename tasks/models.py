from django.db import models

# Create your models here.

from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

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
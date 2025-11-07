"""Migration to remove 'marca' field from Producto model."""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_ingresoefectivo_cantidad_producto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='marca',
        ),
    ]

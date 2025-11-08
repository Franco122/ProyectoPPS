"""Create Venta and VentaItem models."""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_remove_producto_marca'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(max_digits=12, decimal_places=2)),
                ('descripcion', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='VentaItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.DecimalField(max_digits=10, decimal_places=2)),
                ('producto', models.ForeignKey(on_delete=models.PROTECT, to='tasks.producto')),
                ('venta', models.ForeignKey(on_delete=models.CASCADE, related_name='items', to='tasks.venta')),
            ],
        ),
    ]

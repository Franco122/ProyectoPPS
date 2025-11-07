from django.db import connection
import csv

# Este script se debe ejecutar con: python manage.py shell < scripts/export_marca.py
# Exporta id, nombre, marca de la tabla tasks_producto a marca_backup.csv

with connection.cursor() as cursor:
    try:
        cursor.execute("SELECT id, nombre, marca FROM tasks_producto")
        rows = cursor.fetchall()
    except Exception as e:
        print('Error al leer la tabla tasks_producto:', e)
        rows = []

out_path = 'marca_backup.csv'
with open(out_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'nombre', 'marca'])
    for r in rows:
        writer.writerow(r)

print(f'Exportadas {len(rows)} filas a {out_path}')

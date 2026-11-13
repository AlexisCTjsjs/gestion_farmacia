from django.contrib import admin
from .models import Categoria, Laboratorio, Cliente, Medico, Medicamento, RecetaMedica, Venta

for modelo in (Categoria, Laboratorio, Cliente, Medico, Medicamento, RecetaMedica, Venta):
    admin.site.register(modelo)

admin.site.site_header = 'FarmaSalud — Administración Farmacéutica'
admin.site.site_title = 'FarmaSalud'
admin.site.index_title = 'Panel de Control Farmacéutico'

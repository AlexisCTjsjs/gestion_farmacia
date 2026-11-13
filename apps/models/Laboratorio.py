from django.db import models


class Laboratorio(models.Model):
    nombre = models.CharField('Nombre del laboratorio o fabricante', max_length=120, unique=True)
    ruc = models.CharField('RUC / Registro fiscal', max_length=20, blank=True)
    telefono = models.CharField('Teléfono de contacto', max_length=30, blank=True)
    email = models.EmailField('Correo electrónico', blank=True)
    direccion = models.CharField('Dirección o sede', max_length=200, blank=True)
    activo = models.BooleanField('Proveedor activo', default=True)

    class Meta:
        db_table = 'laboratorios'
        ordering = ['nombre']
        verbose_name = 'Laboratorio / Proveedor'
        verbose_name_plural = 'Laboratorios y Proveedores'

    def __str__(self):
        return self.nombre


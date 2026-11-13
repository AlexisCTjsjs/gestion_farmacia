from django.db import models


class Categoria(models.Model):
    nombre = models.CharField('Nombre de la categoría', max_length=100, unique=True)
    descripcion = models.TextField('Descripción o uso terapéutico', blank=True)
    activo = models.BooleanField('Activo', default=True)

    class Meta:
        db_table = 'categorias'
        ordering = ['nombre']
        verbose_name = 'Categoría Farmacéutica'
        verbose_name_plural = 'Categorías Farmacéuticas'

    def __str__(self):
        return self.nombre


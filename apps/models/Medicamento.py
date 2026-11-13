from django.db import models
from .Categoria import Categoria
from .Laboratorio import Laboratorio


class Medicamento(models.Model):
    PRESENTACIONES = [
        ('Tabletas', 'Tabletas / Comprimidos'),
        ('Capsulas', 'Cápsulas'),
        ('Jarabe', 'Jarabe / Solución oral'),
        ('Suspension', 'Suspensión'),
        ('Gotas', 'Gotas oftálmicas / óticas / orales'),
        ('Inyectable', 'Ampolla / Inyectable'),
        ('Crema', 'Crema / Pomada / Ungüento'),
        ('Aerosol', 'Aerosol / Inhalador'),
        ('Gel', 'Gel tópico'),
        ('Supositorio', 'Supositorio'),
        ('Insumo', 'Insumo / Material médico'),
    ]

    codigo_barras = models.CharField('Código de barras / SKU', max_length=50, blank=True)
    nombre = models.CharField('Nombre comercial', max_length=150)
    principio_activo = models.CharField('Principio activo (Genérico)', max_length=150, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='medicamentos', verbose_name='Categoría')
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True, blank=True, related_name='medicamentos', verbose_name='Laboratorio / Fabricante')
    presentacion = models.CharField('Presentación', max_length=50, choices=PRESENTACIONES, default='Tabletas')
    concentracion = models.CharField('Concentración', max_length=80, blank=True, help_text='Ej: 500 mg, 1 g, 250 mg / 5 mL')
    precio_compra = models.DecimalField('Precio de costo (S/)', max_digits=10, decimal_places=2, default=0.00)
    precio_venta = models.DecimalField('Precio de venta al público (S/)', max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField('Stock actual en farmacia', default=0)
    stock_minimo = models.PositiveIntegerField('Stock mínimo de alerta', default=5)
    lote = models.CharField('N.° de Lote', max_length=50, blank=True)
    fecha_vencimiento = models.DateField('Fecha de vencimiento', null=True, blank=True)
    requiere_receta = models.BooleanField('¿Venta bajo receta médica?', default=False)
    instrucciones = models.TextField('Instrucciones de conservación o uso', blank=True)
    activo = models.BooleanField('Disponible para la venta', default=True)

    class Meta:
        db_table = 'medicamentos'
        ordering = ['nombre']
        verbose_name = 'Medicamento / Fármaco'
        verbose_name_plural = 'Medicamentos y Fármacos'

    def __str__(self):
        conc = f' {self.concentracion}' if self.concentracion else ''
        return f'{self.nombre}{conc} ({self.presentacion}) - Stock: {self.stock}'

    @property
    def stock_bajo(self):
        return self.stock <= self.stock_minimo

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .Cliente import Cliente
from .Medicamento import Medicamento


class Venta(models.Model):
    METODOS_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta de Débito / Crédito'),
        ('Yape/Plin', 'Billetera Digital (Yape / Plin)'),
        ('Transferencia', 'Transferencia Bancaria'),
    ]
    TIPOS_COMPROBANTE = [
        ('Boleta', 'Boleta de Venta Electrónica'),
        ('Factura', 'Factura Electrónica'),
        ('Ticket', 'Ticket de Venta'),
    ]
    ESTADOS = [
        ('Completada', 'Completada / Pagada'),
        ('Anulada', 'Anulada'),
    ]

    numero_comprobante = models.CharField('N.° de Comprobante / Ticket', max_length=50, unique=True)
    tipo_comprobante = models.CharField('Tipo de comprobante', max_length=20, choices=TIPOS_COMPROBANTE, default='Boleta')
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas', verbose_name='Cliente / Paciente (Opcional)')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT, related_name='ventas', verbose_name='Medicamento / Fármaco')
    cantidad = models.PositiveIntegerField('Cantidad vendida', default=1)
    precio_unitario = models.DecimalField('Precio Unitario (S/)', max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField('Total Cobrado (S/)', max_digits=10, decimal_places=2, default=0.00)
    metodo_pago = models.CharField('Método de pago', max_length=20, choices=METODOS_PAGO, default='Efectivo')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas_atendidas', verbose_name='Farmacéutico / Atendido por')
    fecha = models.DateTimeField('Fecha y hora de venta', default=timezone.now)
    estado = models.CharField('Estado', max_length=20, choices=ESTADOS, default='Completada')
    observaciones = models.TextField('Observaciones o N.° de operación', blank=True)

    class Meta:
        db_table = 'ventas'
        ordering = ['-fecha']
        verbose_name = 'Venta / Dispensación'
        verbose_name_plural = 'Ventas y Dispensaciones'

    def __str__(self):
        return f'{self.tipo_comprobante} #{self.numero_comprobante} - S/ {self.total}'

    def save(self, *args, **kwargs):
        if not self.total or self.total == 0:
            self.total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)


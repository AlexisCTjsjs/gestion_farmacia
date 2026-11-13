from django.db import models
from django.utils import timezone
from .Cliente import Cliente
from .Medico import Medico
from .Medicamento import Medicamento


class RecetaMedica(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente de dispensación'),
        ('Dispensada', 'Dispensada / Despachada'),
        ('Anulada', 'Anulada / Vencida'),
    ]

    numero_receta = models.CharField('N.° de Receta / Folio', max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='recetas', verbose_name='Paciente / Cliente')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='recetas', verbose_name='Médico prescriptor')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT, related_name='recetas', verbose_name='Medicamento prescrito')
    dosis = models.CharField('Dosis (ej: 1 tableta)', max_length=100)
    frecuencia = models.CharField('Frecuencia (ej: cada 8 horas después de comidas)', max_length=120)
    duracion = models.CharField('Duración del tratamiento (ej: 7 días)', max_length=100)
    diagnostico = models.CharField('Diagnóstico médico / Motivo', max_length=200, blank=True)
    indicaciones = models.TextField('Indicaciones adicionales de posología', blank=True)
    fecha_emision = models.DateField('Fecha de emisión', default=timezone.now)
    fecha_vencimiento = models.DateField('Fecha de vencimiento de receta', null=True, blank=True)
    estado = models.CharField('Estado de dispensación', max_length=20, choices=ESTADOS, default='Pendiente')

    class Meta:
        db_table = 'recetas_medicas'
        ordering = ['-fecha_emision']
        verbose_name = 'Receta Médica'
        verbose_name_plural = 'Recetas Médicas'

    def __str__(self):
        return f'Receta #{self.numero_receta} - {self.cliente} ({self.medicamento.nombre})'


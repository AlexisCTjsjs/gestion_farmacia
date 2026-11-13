from django.db import models


class Medico(models.Model):
    nombre = models.CharField('Nombres', max_length=100)
    apellido = models.CharField('Apellidos', max_length=100)
    colegiatura = models.CharField('N.° Colegiatura Médica (CMP)', max_length=50, unique=True)
    especialidad = models.CharField('Especialidad', max_length=100, default='Medicina General')
    telefono = models.CharField('Teléfono / Contacto', max_length=30, blank=True)
    clinica_hospital = models.CharField('Clínica, Hospital o Centro de Salud', max_length=150, blank=True)
    activo = models.BooleanField('Médico habilitado', default=True)

    class Meta:
        db_table = 'medicos'
        ordering = ['apellido', 'nombre']
        verbose_name = 'Médico Prescriptor'
        verbose_name_plural = 'Médicos Prescriptores'

    def __str__(self):
        return f'Dr(a). {self.nombre} {self.apellido} (CMP: {self.colegiatura})'


from django.db import models


class Cliente(models.Model):
    nombre = models.CharField('Nombres', max_length=100)
    apellido = models.CharField('Apellidos', max_length=100)
    dni = models.CharField('DNI / Cédula / Documento', max_length=20, unique=True)
    telefono = models.CharField('Teléfono / Celular', max_length=30, blank=True)
    email = models.EmailField('Correo electrónico', blank=True)
    direccion = models.CharField('Dirección', max_length=200, blank=True)
    alergias = models.CharField('Alergias o contraindicaciones', max_length=250, blank=True, help_text='Ej: Alérgico a penicilina, intolerancia a la lactosa, hipertenso, etc.')

    class Meta:
        db_table = 'clientes'
        ordering = ['apellido', 'nombre']
        verbose_name = 'Cliente / Paciente'
        verbose_name_plural = 'Clientes y Pacientes'

    def __str__(self):
        return f'{self.nombre} {self.apellido} (DNI: {self.dni})'


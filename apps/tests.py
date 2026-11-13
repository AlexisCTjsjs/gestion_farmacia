from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from datetime import date
from .models import Categoria, Laboratorio, Cliente, Medico, Medicamento, RecetaMedica, Venta


class FarmaciaTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='farmaceutico', password='ClaveSegura123#')
        self.cat = Categoria.objects.create(nombre='Analgésicos', descripcion='Alivio del dolor')
        self.lab = Laboratorio.objects.create(nombre='Laboratorios Bagó', ruc='20100123456')
        self.cli = Cliente.objects.create(nombre='Juan', apellido='Pérez', dni='12345678', telefono='987654321')
        self.med = Medico.objects.create(nombre='Carlos', apellido='Gómez', colegiatura='CMP-45892', especialidad='Medicina Interna')
        self.prod = Medicamento.objects.create(
            nombre='Paracetamol',
            principio_activo='Paracetamol',
            categoria=self.cat,
            laboratorio=self.lab,
            presentacion='Tabletas',
            concentracion='500 mg',
            precio_compra=0.50,
            precio_venta=1.20,
            stock=100
        )
        self.rec = RecetaMedica.objects.create(
            numero_receta='REC-001',
            cliente=self.cli,
            medico=self.med,
            medicamento=self.prod,
            dosis='1 tableta',
            frecuencia='Cada 8 horas',
            duracion='3 días'
        )
        self.venta = Venta.objects.create(
            numero_comprobante='B001-0001',
            tipo_comprobante='Boleta',
            cliente=self.cli,
            medicamento=self.prod,
            cantidad=2,
            precio_unitario=1.20,
            total=2.40,
            usuario=self.usuario
        )

    def test_login_requerido(self):
        r = self.client.get(reverse('listado', args=['medicamentos']))
        self.assertEqual(r.status_code, 302)

    def test_crud_de_siete_secciones_farmacia(self):
        self.client.force_login(self.usuario)
        secciones = ['medicamentos', 'ventas', 'recetas', 'clientes', 'categorias', 'laboratorios', 'medicos']
        for seccion in secciones:
            self.assertEqual(self.client.get(reverse('listado', args=[seccion])).status_code, 200)
            self.assertEqual(self.client.get(reverse('nuevo', args=[seccion])).status_code, 200)

        elementos = [
            ('medicamentos', self.prod),
            ('ventas', self.venta),
            ('recetas', self.rec),
            ('clientes', self.cli),
            ('categorias', self.cat),
            ('laboratorios', self.lab),
            ('medicos', self.med),
        ]
        for seccion, obj in elementos:
            self.assertEqual(self.client.get(reverse('editar', args=[seccion, obj.pk])).status_code, 200)

    def test_reporte_e_impresiones_farmacia(self):
        self.client.force_login(self.usuario)
        self.assertEqual(self.client.get(reverse('reporte')).status_code, 200)
        for seccion, obj in [('ventas', self.venta), ('recetas', self.rec)]:
            self.assertEqual(self.client.get(reverse('imprimir', args=[seccion, obj.pk])).status_code, 200)

    def test_eliminar_no_permitido_por_get(self):
        self.client.force_login(self.usuario)
        self.assertEqual(self.client.get(reverse('eliminar', args=['recetas', self.rec.pk])).status_code, 405)

    def test_proteger_medicamento_con_recetas_o_ventas(self):
        self.client.force_login(self.usuario)
        resp = self.client.post(reverse('eliminar', args=['medicamentos', self.prod.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Medicamento.objects.filter(pk=self.prod.pk).exists())

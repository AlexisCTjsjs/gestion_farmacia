from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.db.models import Q, F, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    CategoriaForm, LaboratorioForm, ClienteForm, MedicoForm,
    MedicamentoForm, RecetaMedicaForm, VentaForm, RegistroForm
)
from .models import (
    Categoria, Laboratorio, Cliente, Medico,
    Medicamento, RecetaMedica, Venta
)

# Secciones del sistema de gestión farmacéutica
SECCIONES = {
    'medicamentos': {
        'modelo': Medicamento,
        'formulario': MedicamentoForm,
        'titulo': 'Medicamentos y Fármacos',
        'singular': 'Medicamento',
        'icono': '💊',
        'campos': ['nombre', 'principio_activo', 'presentacion', 'concentracion', 'precio_venta', 'stock', 'requiere_receta', 'activo']
    },
    'ventas': {
        'modelo': Venta,
        'formulario': VentaForm,
        'titulo': 'Ventas y Dispensación',
        'singular': 'Venta',
        'icono': '🛒',
        'campos': ['numero_comprobante', 'tipo_comprobante', 'cliente', 'medicamento', 'cantidad', 'total', 'metodo_pago', 'estado']
    },
    'recetas': {
        'modelo': RecetaMedica,
        'formulario': RecetaMedicaForm,
        'titulo': 'Recetas Médicas',
        'singular': 'Receta',
        'icono': '📋',
        'campos': ['numero_receta', 'cliente', 'medico', 'medicamento', 'dosis', 'frecuencia', 'duracion', 'estado']
    },
    'clientes': {
        'modelo': Cliente,
        'formulario': ClienteForm,
        'titulo': 'Clientes y Pacientes',
        'singular': 'Cliente',
        'icono': '👥',
        'campos': ['nombre', 'apellido', 'dni', 'telefono', 'email', 'alergias']
    },
    'categorias': {
        'modelo': Categoria,
        'formulario': CategoriaForm,
        'titulo': 'Categorías Farmacéuticas',
        'singular': 'Categoría',
        'icono': '🏷️',
        'campos': ['nombre', 'descripcion', 'activo']
    },
    'laboratorios': {
        'modelo': Laboratorio,
        'formulario': LaboratorioForm,
        'titulo': 'Laboratorios y Proveedores',
        'singular': 'Laboratorio',
        'icono': '🏭',
        'campos': ['nombre', 'ruc', 'telefono', 'email', 'direccion', 'activo']
    },
    'medicos': {
        'modelo': Medico,
        'formulario': MedicoForm,
        'titulo': 'Médicos Prescriptores',
        'singular': 'Médico',
        'icono': '👨‍⚕️',
        'campos': ['nombre', 'apellido', 'colegiatura', 'especialidad', 'telefono', 'clinica_hospital', 'activo']
    },
}

BUSQUEDAS = {
    'medicamentos': ['nombre', 'principio_activo', 'codigo_barras', 'lote'],
    'ventas': ['numero_comprobante', 'cliente__nombre', 'cliente__apellido', 'medicamento__nombre'],
    'recetas': ['numero_receta', 'cliente__nombre', 'cliente__apellido', 'medico__apellido', 'medicamento__nombre'],
    'clientes': ['nombre', 'apellido', 'dni', 'telefono'],
    'categorias': ['nombre', 'descripcion'],
    'laboratorios': ['nombre', 'ruc', 'telefono'],
    'medicos': ['nombre', 'apellido', 'colegiatura', 'especialidad'],
}


def ingresar(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    formulario = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and formulario.is_valid():
        login(request, formulario.get_user())
        if not request.POST.get('recordarme'):
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(60 * 60 * 24 * 14)
        return redirect('inicio')
    return render(request, 'control/login.html', {
        'formulario': formulario,
        'registro_abierto': settings.REGISTRATION_OPEN
    })


def registro(request):
    if not settings.REGISTRATION_OPEN:
        raise Http404('Registro deshabilitado. Contacta al administrador.')
    if request.user.is_authenticated:
        return redirect('inicio')
    formulario = RegistroForm(request.POST or None)
    if request.method == 'POST' and formulario.is_valid():
        usuario = formulario.save(commit=False)
        usuario.email = formulario.cleaned_data['email']
        usuario.save()
        login(request, usuario)
        request.session.set_expiry(0)
        messages.success(request, 'Cuenta de empleado creada correctamente.')
        return redirect('inicio')
    return render(request, 'control/registro.html', {'formulario': formulario})


@login_required
@require_POST
def salir(request):
    logout(request)
    return redirect('login')


@login_required
def inicio(request):
    resumen = [
        {
            'titulo': item['titulo'],
            'total': item['modelo'].objects.count(),
            'clave': nombre,
            'icono': item.get('icono', '📁'),
            'singular': item.get('singular', 'Registro'),
        }
        for nombre, item in SECCIONES.items()
    ]
    medicamentos_recientes = Medicamento.objects.select_related('categoria', 'laboratorio').order_by('-id')[:6]
    ventas_recientes = Venta.objects.select_related('cliente', 'medicamento', 'usuario').order_by('-fecha')[:6]
    recetas_recientes = RecetaMedica.objects.select_related('cliente', 'medico', 'medicamento').order_by('-fecha_emision')[:6]
    stock_bajo_count = Medicamento.objects.filter(stock__lte=F('stock_minimo'), activo=True).count()

    return render(request, 'control/inicio.html', {
        'resumen': resumen,
        'medicamentos_recientes': medicamentos_recientes,
        'ventas_recientes': ventas_recientes,
        'recetas_recientes': recetas_recientes,
        'stock_bajo_count': stock_bajo_count,
    })


@login_required
def listado(request, seccion):
    info = SECCIONES.get(seccion)
    if info is None:
        raise Http404('Módulo no disponible en farmacia')
    objetos = info['modelo'].objects.all()

    if seccion == 'medicamentos':
        objetos = objetos.select_related('categoria', 'laboratorio')
    elif seccion == 'ventas':
        objetos = objetos.select_related('cliente', 'medicamento', 'usuario')
    elif seccion == 'recetas':
        objetos = objetos.select_related('cliente', 'medico', 'medicamento')

    q = request.GET.get('q', '').strip()[:100]
    if q:
        filtro = Q()
        for campo in BUSQUEDAS.get(seccion, []):
            filtro |= Q(**{campo + '__icontains': q})
        objetos = objetos.filter(filtro)

    objetos = objetos[:300]
    filas = [[getattr(obj, campo) for campo in info['campos']] for obj in objetos]
    datos = list(zip(objetos, filas))
    return render(request, 'control/listado.html', {
        'info': info,
        'seccion': seccion,
        'datos': datos,
        'q': q
    })


@login_required
def guardar(request, seccion, pk=None):
    info = SECCIONES.get(seccion)
    if info is None:
        raise Http404('Módulo no disponible en farmacia')
    objeto = get_object_or_404(info['modelo'], pk=pk) if pk else None
    formulario = info['formulario'](request.POST or None, instance=objeto)

    # Si es una nueva venta y no se asignó usuario, asignar el actual
    if seccion == 'ventas' and not pk and request.method == 'GET' and 'usuario' in formulario.fields:
        formulario.initial['usuario'] = request.user

    if request.method == 'POST' and formulario.is_valid():
        try:
            guardado = formulario.save(commit=False)
            if seccion == 'ventas' and not guardado.usuario:
                guardado.usuario = request.user
            guardado.save()
            formulario.save_m2m() if hasattr(formulario, 'save_m2m') else None
            messages.success(request, f'{info["singular"]} guardado correctamente.')
            return redirect('listado', seccion=seccion)
        except IntegrityError:
            formulario.add_error(None, 'Error al guardar: código o dato duplicado en el sistema.')

    return render(request, 'control/formulario.html', {
        'formulario': formulario,
        'info': info,
        'seccion': seccion,
        'objeto': objeto
    })


@login_required
@require_POST
def eliminar(request, seccion, pk):
    info = SECCIONES.get(seccion)
    if info is None:
        raise Http404('Módulo no disponible en farmacia')
    objeto = get_object_or_404(info['modelo'], pk=pk)
    from django.db.models.deletion import ProtectedError
    try:
        objeto.delete()
        messages.success(request, f'{info["singular"]} eliminado del sistema.')
    except ProtectedError:
        messages.error(request, 'No se puede eliminar: tiene ventas o recetas asociadas en la farmacia.')
    return redirect('listado', seccion=seccion)


@login_required
def imprimir(request, seccion, pk):
    if seccion not in ('ventas', 'recetas'):
        raise Http404('Documento no disponible para impresión')
    modelo = SECCIONES[seccion]['modelo']
    objeto = get_object_or_404(modelo, pk=pk)
    return render(request, 'control/impresion.html', {
        'objeto': objeto,
        'seccion': seccion
    })


@login_required
def reporte(request):
    ventas = Venta.objects.select_related('cliente', 'medicamento', 'usuario').all()
    inicio = request.GET.get('desde', '')
    fin = request.GET.get('hasta', '')
    metodo = request.GET.get('metodo', '')
    tipo = request.GET.get('tipo', '')
    from datetime import date
    try:
        if inicio:
            ventas = ventas.filter(fecha__date__gte=date.fromisoformat(inicio))
        if fin:
            ventas = ventas.filter(fecha__date__lte=date.fromisoformat(fin))
    except ValueError:
        messages.error(request, 'Las fechas deben tener formato AAAA-MM-DD.')
        return redirect('reporte')

    if metodo:
        ventas = ventas.filter(metodo_pago=metodo)
    if tipo:
        ventas = ventas.filter(tipo_comprobante=tipo)

    total_recaudado = ventas.filter(estado='Completada').aggregate(suma=Sum('total'))['suma'] or 0.00

    return render(request, 'control/reporte.html', {
        'ventas': ventas[:500],
        'desde': inicio,
        'hasta': fin,
        'metodo': metodo,
        'tipo': tipo,
        'metodos_pago': Venta.METODOS_PAGO,
        'tipos_comprobante': Venta.TIPOS_COMPROBANTE,
        'total_recaudado': total_recaudado,
    })

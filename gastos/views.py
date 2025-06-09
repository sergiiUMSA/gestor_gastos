from django.shortcuts import render, redirect, get_object_or_404
from .forms import TransaccionForm
from .models import Transaccion
from django.db.models import Sum
from django.http import JsonResponse
from django.utils.timezone import now
from decimal import Decimal
from django.http import HttpResponse
from .models import Presupuesto
from .forms import PresupuestoForm
from django.contrib import messages
from django.shortcuts import render
from datetime import date
from .models import Transaccion, Presupuesto
from django.db.models.functions import TruncMonth

def lista_rutas(request):
    contenido = """
    <pre>
Using the URLconf defined in gestor_gastos.urls, Django tried these URL patterns, in this order:

admin/
inicio/
nueva/
lista/
grafico/
resumen/
    </pre>
    """
    return HttpResponse(contenido)


def resumen_mes(request):
    from django.utils.timezone import now
    hoy = now()

    presupuesto = {
        'mes': hoy.month,
        'anio': hoy.year,
        'monto': Decimal('1000.00'),  # Cambiar a Decimal
    }

    gastos_mes = Transaccion.objects.filter(
        fecha__year=hoy.year,
        fecha__month=hoy.month
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')  # Asegurarse que sea Decimal

    disponible = presupuesto['monto'] - gastos_mes  # Ambas son Decimal ahora

    alerta = None
    if gastos_mes > presupuesto['monto']:
        alerta = "Has excedido tu presupuesto mensual."
    elif gastos_mes >= presupuesto['monto'] * Decimal('0.8'):
        alerta = "Estás cerca de tu límite presupuestario."

    contexto = {
        'presupuesto': presupuesto,
        'gastos_mes': gastos_mes,
        'disponible': disponible,
        'alerta': alerta,
    }

    return render(request, 'gastos/resumen_mes.html', contexto)

# El resto de las funciones quedan igual (agregar_transaccion, lista_transacciones, etc.)

def inicio(request):
    return render(request, 'gastos/home.html')

def agregar_transaccion(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige al inicio (puedes cambiarlo si quieres)
    else:
        form = TransaccionForm()
    return render(request, 'gastos/agregar_transaccion.html', {'form': form})

def lista_transacciones(request):
    transacciones = Transaccion.objects.all().order_by('-fecha')  # más recientes primero
    return render(request, 'gastos/lista_transacciones.html', {'transacciones': transacciones})


def grafico_gastos(request):
    datos = Transaccion.objects.values('categoria').annotate(total=Sum('monto'))
    categorias = [item['categoria'] for item in datos]
    montos = [float(item['total']) for item in datos]
    return JsonResponse({'categorias': categorias, 'montos': montos})

def vista_grafico(request):
    return render(request, 'gastos/grafico.html')

#eliminar 
def eliminar_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(Transaccion, id=transaccion_id)
    transaccion.delete()
    return redirect('lista_transacciones')
#editar
def editar_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(Transaccion, id=transaccion_id)
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            form.save()
            return redirect('lista_transacciones')
    else:
        form = TransaccionForm(instance=transaccion)
    return render(request, 'gastos/editar_transaccion.html', {'form': form})
def agregar_presupuesto(request):
    if request.method == 'POST':
        form = PresupuestoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Presupuesto agregado correctamente.')
            return redirect('ver_presupuesto')
    else:
        form = PresupuestoForm()
    return render(request, 'gastos/agregar_presupuesto.html', {'form': form})

def ver_presupuesto(request):
    presupuestos = Presupuesto.objects.all().order_by('-anio', 'mes')
    return render(request, 'gastos/ver_presupuesto.html', {'presupuestos': presupuestos})
def resumen_presupuesto(request):
    hoy = date.today()
    mes_actual = hoy.month
    anio_actual = hoy.year

    # Buscar el presupuesto del mes actual
    presupuesto_actual = Presupuesto.objects.filter(mes=mes_actual, anio=anio_actual).first()

    # Sumar los gastos del mes actual
    gastos_mes = Transaccion.objects.filter(
        fecha__month=mes_actual,
        fecha__year=anio_actual
    ).aggregate(total=Sum('monto'))['total'] or 0

    restante = (presupuesto_actual.monto - gastos_mes) if presupuesto_actual else 0

    return render(request, 'gastos/resumen.html', {
        'presupuesto': presupuesto_actual,
        'gastado': gastos_mes,
        'restante': restante,
        'mes': mes_actual,
        'anio': anio_actual,
    })

def grafico_mensual(request):
    anio_actual = date.today().year
    gastos = (
        Transaccion.objects
        .filter(fecha__year=anio_actual)
        .annotate(mes=TruncMonth('fecha'))
        .values('mes')
        .annotate(total=Sum('monto'))
        .order_by('mes')
    )

    etiquetas = [g['mes'].strftime('%B') for g in gastos]  # Ej: Enero, Febrero
    montos = [float(g['total']) for g in gastos]

    return JsonResponse({'meses': etiquetas, 'montos': montos})

from django.shortcuts import render

def vista_grafico_mensual(request):
    return render(request, 'gastos/grafico_mensual.html')
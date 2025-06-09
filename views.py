from django.shortcuts import render, redirect, get_object_or_404
from .forms import TransaccionForm
from .models import Transaccion
from django.db.models import Sum
from django.http import JsonResponse
from django.utils.timezone import now
from decimal import Decimal

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
from django.shortcuts import render, redirect
from .forms import TransaccionForm, PresupuestoForm, RegistroForm # type: ignore
from .models import  Transaccion, Categoria, Presupuesto, CategoriaGasto
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime


# Vista para registrar una transacción
def registrar_transaccion(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            transaccion = form.save(commit=False)
            transaccion.usuario = request.user  # Asignar al usuario logueado
            transaccion.save()
            return redirect('listar_transacciones')
    else:
        form = TransaccionForm()
    return render(request, 'gastos/registrar_transaccion.html', {'form': form})

# Vista para listar transacciones
def listar_transacciones(request):
    transacciones = Transaccion.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'gastos/listar_transacciones.html', {'transacciones': transacciones})

# Vista para crear un presupuesto mensual
def crear_presupuesto(request):
    if request.method == 'POST':
        form = PresupuestoForm(request.user, request.POST)
        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.usuario = request.user
            presupuesto.save()
            return redirect('listar_presupuestos')
    else:
        form = PresupuestoForm(request.user)
    return render(request, 'crear_presupuesto.html', {'form': form})
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})
@login_required
def listar_transacciones(request):
    transacciones = Transaccion.objects.filter(usuario=request.user)
    return render(request, 'transacciones.html', {'transacciones': transacciones})

def crear_transaccion(request):
    if request.method == 'POST':
        form = TransaccionForm(request.user, request.POST)  # Pasa el usuario
        if form.is_valid():
            transaccion = form.save(commit=False)
            transaccion.usuario = request.user
            transaccion.save()
            return redirect('listar_transacciones')
    else:
        form = TransaccionForm(request.user)  # Pasa el usuario
    return render(request, 'crear_transaccion.html', {'form': form})
def listar_transacciones(request):
    # Obtener todas las transacciones del usuario
    transacciones = Transaccion.objects.filter(usuario=request.user)
    
    # Obtener parámetros GET (filtros)
    categoria_id = request.GET.get('categoria')
    mes = request.GET.get('mes')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    # Aplicar filtros si existen
    if categoria_id:
        transacciones = transacciones.filter(categoria__id=categoria_id)
    if mes:
        transacciones = transacciones.filter(fecha__month=mes)
    if fecha_inicio and fecha_fin:
        transacciones = transacciones.filter(
            fecha__range=(fecha_inicio, fecha_fin)
        )
    
    # Obtener categorías para mostrar en el dropdown
    categorias = Categoria.objects.filter(usuario=request.user)
    
    return render(request, 'transacciones.html', {
        'transacciones': transacciones,
        'categorias': categorias,
    })    
def dashboard(request):
    # Datos para el gráfico de gastos por categoría (último mes)
    mes_actual = datetime.now().month
    gastos_por_categoria = (
        Transaccion.objects
        .filter(usuario=request.user, fecha__month=mes_actual)
        .values('categoria__nombre')
        .annotate(total=Sum('monto'))
        .order_by('-total')
    )

    # Datos para el gráfico de presupuesto vs gastos
    presupuestos = Presupuesto.objects.filter(
        usuario=request.user,
        mes__month=mes_actual
    )
    datos_presupuesto = []
    for presupuesto in presupuestos:
        gasto_categoria = Transaccion.objects.filter(
            usuario=request.user,
            categoria=presupuesto.categoria,
            fecha__month=mes_actual
        ).aggregate(total=Sum('monto'))['total'] or 0
        datos_presupuesto.append({
            'categoria': presupuesto.categoria.nombre,
            'presupuesto': presupuesto.monto,
            'gasto': gasto_categoria,
        })

    return render(request, 'dashboard.html', {
        'gastos_por_categoria': gastos_por_categoria,
        'datos_presupuesto': datos_presupuesto,
    })



def grafico_gastos_categoria(request):
    categorias = CategoriaGasto.objects.all()
    data = []
    for cat in categorias:
        total = Transaccion.objects.filter(categoria=cat, usuario=request.user).aggregate(Sum('monto'))['monto__sum'] or 0
        data.append({'categoria': cat.nombre, 'total': total})
    return render(request, 'grafico_categoria.html', {'data': data})

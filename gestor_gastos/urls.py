from django.contrib import admin
from django.urls import path
from gastos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.lista_rutas),  # <-- página principal como una lista de rutas
    path('inicio/', views.inicio, name='inicio'),
    path('nueva/', views.agregar_transaccion, name='agregar_transaccion'),
    path('lista/', views.lista_transacciones, name='lista_transacciones'),
    path('grafico/', views.vista_grafico, name='vista_grafico'),
    path('api/grafico/', views.grafico_gastos, name='grafico_gastos'),
    path('resumen/', views.resumen_mes, name='resumen_mes'),
    path('eliminar/<int:transaccion_id>/', views.eliminar_transaccion, name='eliminar_transaccion'),
    path('editar/<int:transaccion_id>/', views.editar_transaccion, name='editar_transaccion'),
    path('presupuesto/nuevo/', views.agregar_presupuesto, name='agregar_presupuesto'),
    path('presupuesto/', views.ver_presupuesto, name='ver_presupuesto'),
    path('grafico-mensual/', views.vista_grafico_mensual, name='vista_grafico_mensual'),
    path('api/grafico-mensual/', views.grafico_mensual, name='grafico_mensual'),
]

from django.contrib import admin
from .models import CategoriaGasto, Presupuesto, Transaccion

admin.site.register(CategoriaGasto)
admin.site.register(Presupuesto)
admin.site.register(Transaccion)

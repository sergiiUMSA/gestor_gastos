from django.db import models
from django.contrib.auth.models import User  # Usamos el sistema de usuarios de Django

class CategoriaGasto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}"

class Presupuesto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    mes = models.DateField()  # Puedes usar el primer día del mes como referencia
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Presupuesto {self.mes.strftime('%B %Y')} - {self.usuario.username}"

class Transaccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaGasto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.categoria.nombre} - ${self.cantidad} - {self.fecha}"

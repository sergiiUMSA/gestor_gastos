from django.db import models

class Transaccion(models.Model):
    categoria = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.categoria} - {self.monto} Bs."

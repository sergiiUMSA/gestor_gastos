from django import forms
from .models import Transaccion
from .models import Presupuesto

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['categoria', 'monto', 'descripcion']

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['mes', 'anio', 'monto']
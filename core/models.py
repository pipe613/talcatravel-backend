from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Tour(models.Model):
    nombre = models.CharField(max_length=200)
    destino = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_dias = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    fecha = models.DateField()
    cantidad_pasajeros = models.PositiveIntegerField(default=1)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Nuevo campo

    def __str__(self):
        return f"Reserva de {self.tour.nombre} - Total: ${self.precio_total}"
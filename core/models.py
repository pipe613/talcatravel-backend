from django.db import models

class Tour(models.Model):
    nombre = models.CharField(max_length=200)
    destino = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_dias = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    fecha = models.DateField()
    cantidad_pasajeros = models.PositiveIntegerField(default=1)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Reserva de {self.tour.nombre} - Total: ${self.precio_total}"
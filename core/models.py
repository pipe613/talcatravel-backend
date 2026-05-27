from django.db import models
from django.db.models import Sum

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)  # Guardará la clave de forma segura

    def __str__(self):
        return self.nombre

class Tour(models.Model):
    nombre = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    duracion_dias = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cupo_maximo = models.IntegerField(default=20)  # Control de disponibilidad para el escenario

    def __str__(self):
        return self.nombre

    def cupo_ocupado(self, exclude_reserva_id=None):
        reservas = Reserva.objects.filter(tour=self)
        if exclude_reserva_id is not None:
            reservas = reservas.exclude(pk=exclude_reserva_id)
        return reservas.aggregate(total=Sum('cantidad_pasajeros')).get('total') or 0

    def cupo_restante(self, exclude_reserva_id=None):
        return self.cupo_maximo - self.cupo_ocupado(exclude_reserva_id=exclude_reserva_id)

    def puede_reservar(self, cantidad, exclude_reserva_id=None):
        return self.cupo_ocupado(exclude_reserva_id=exclude_reserva_id) + cantidad <= self.cupo_maximo

class Reserva(models.Model):
    # Vinculamos directamente a nuestra tabla propia de usuarios
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    fecha = models.DateField()
    cantidad_pasajeros = models.IntegerField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Reserva {self.id} -> {self.usuario.nombre} en {self.tour.nombre}"
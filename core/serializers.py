from rest_framework import serializers
from .models import Tour, Reserva

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'tour', 'fecha', 'cantidad_pasajeros', 'precio_total'] # Incluido precio_total
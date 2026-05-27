from rest_framework import serializers
from .models import Usuario, Tour, Reserva

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

    def validate(self, attrs):
        tour = attrs.get('tour') or getattr(self.instance, 'tour', None)
        cantidad = attrs.get('cantidad_pasajeros')
        if cantidad is None:
            cantidad = getattr(self.instance, 'cantidad_pasajeros', 1)

        if tour is None:
            return attrs

        exclude_reserva_id = getattr(self.instance, 'pk', None)
        if not tour.puede_reservar(cantidad, exclude_reserva_id=exclude_reserva_id):
            restante = tour.cupo_restante(exclude_reserva_id=exclude_reserva_id)
            raise serializers.ValidationError({
                'cantidad_pasajeros': f'Cupo excedido. Solo quedan {restante} cupos disponibles para este tour.'
            })

        return attrs
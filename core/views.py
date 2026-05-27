from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from .models import Tour, Reserva, Usuario
from .serializers import TourSerializer, ReservaSerializer, UsuarioSerializer

# API ViewSets para la app móvil
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all().order_by('-id')
    serializer_class = ReservaSerializer
    permission_classes = [permissions.AllowAny] 

    def perform_create(self, serializer):
        tour = serializer.validated_data['tour']
        cantidad = serializer.validated_data.get('cantidad_pasajeros', 1)
        total = tour.precio * cantidad
        serializer.save(precio_total=total)

# ==========================================
# VISTAS DEL DASHBOARD WEB ADMINISTRATIVO
# ==========================================

@login_required(login_url='login')
def dashboard(request):
    tours = Tour.objects.all().order_by('id')
    reservas = Reserva.objects.all().order_by('-id')
    return render(request, 'dashboard.html', {'tours': tours, 'reservas': reservas})

# --- Acciones para Tours ---
@login_required(login_url='login')
def crear_tour(request):
    if request.method == 'POST':
        Tour.objects.create(
            nombre=request.POST.get('nombre'),
            destino=request.POST.get('destino'),
            precio=request.POST.get('precio'),
            duracion_dias=request.POST.get('duracion')
        )
    return redirect('dashboard')

@login_required(login_url='login')
def editar_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        tour.nombre = request.POST.get('nombre')
        tour.destino = request.POST.get('destino')
        tour.precio = request.POST.get('precio')
        tour.duracion_dias = request.POST.get('duracion')
        tour.save()
    return redirect('dashboard')

@login_required(login_url='login')
def eliminar_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        tour.delete()
    return redirect('dashboard')

# --- Acciones para Reservas ---
@login_required(login_url='login')
def crear_reserva(request):
    if request.method == 'POST':
        tour_id = request.POST.get('tour')
        tour_obj = get_object_or_404(Tour, id=tour_id)
        cantidad = int(request.POST.get('cantidad_pasajeros', 1))
        
        Reserva.objects.create(
            tour=tour_obj,
            fecha=request.POST.get('fecha'),
            cantidad_pasajeros=cantidad,
            precio_total=tour_obj.precio * cantidad
        )
    return redirect('dashboard')

@login_required(login_url='login')
def editar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        tour_id = request.POST.get('tour')
        tour_obj = get_object_or_404(Tour, id=tour_id)
        cantidad = int(request.POST.get('cantidad_pasajeros', 1))
        
        reserva.tour = tour_obj
        reserva.fecha = request.POST.get('fecha')
        reserva.cantidad_pasajeros = cantidad
        reserva.precio_total = tour_obj.precio * cantidad
        reserva.save()
    return redirect('dashboard')

@login_required(login_url='login')
def eliminar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
    return redirect('dashboard')
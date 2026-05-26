from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from core.views import (
    TourViewSet, ReservaViewSet, dashboard,
    crear_tour, editar_tour, eliminar_tour,
    crear_reserva, editar_reserva, eliminar_reserva
)

router = DefaultRouter()
router.register(r'tours', TourViewSet)
router.register(r'reservas', ReservaViewSet)

urlpatterns = [
    # API para Flutter
    path('api/', include(router.urls)),
    
    # Autenticación tradicional
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Panel de Control unificado
    path('', dashboard, name='dashboard'),
    
    # Acciones de Tours
    path('tours/crear/', crear_tour, name='crear_tour'),
    path('tours/editar/<int:pk>/', editar_tour, name='editar_tour'),
    path('tours/eliminar/<int:pk>/', eliminar_tour, name='eliminar_tour'),
    
    # Acciones de Reservas
    path('reservas/crear/', crear_reserva, name='crear_reserva'),
    path('reservas/editar/<int:pk>/', editar_reserva, name='editar_reserva'),
    path('reservas/eliminar/<int:pk>/', eliminar_reserva, name='eliminar_reserva'),
]
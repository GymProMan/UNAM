
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Página principal
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),





# Espacios Físicos
    path('espacios/', views.lista_espacios, name='lista_espacios'),
    path('espacios/agregar/', views.agregar_espacio, name='agregar_espacio'),
    path('espacios/editar/<int:pk>/', views.editar_espacio, name='editar_espacio'),
    path('espacios/eliminar/<int:pk>/', views.eliminar_espacio, name='eliminar_espacio'),

    # Solicitudes de Espacios
    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),
    path('solicitudes/agregar/', views.agregar_solicitud, name='agregar_solicitud'),
    path('solicitudes/editar/<int:pk>/', views.editar_solicitud, name='editar_solicitud'),
    path('solicitudes/eliminar/<int:pk>/', views.eliminar_solicitud, name='eliminar_solicitud'),





#detalles


path('solicitudes/<int:pk>/', views.detalle_solicitud, name='detalle_solicitud'),





path('api/solicitudes/', views.obtener_solicitudes, name='obtener_solicitudes'),
path('calendario/', views.calendario_solicitudes, name='calendario_solicitudes'),



#--------------------------------------------------------AGREGADOS PARA VER USUARIOS 24/02/25#
path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),


path('cambiar_contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),

]

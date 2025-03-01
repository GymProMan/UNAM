from django.contrib.auth import login, logout, authenticate
from django.db.models import Q

from .forms import AreaCreationForm, CustomLoginForm
from .models import Area
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import EspacioFisico, SolicitudEspacio
from .forms import EspacioFisicoForm, SolicitudEspacioForm

def register(request):
    if request.method == 'POST':
        form = AreaCreationForm(request.POST)
        if form.is_valid():
            area = form.save(commit=False)
            area.set_password(form.cleaned_data['password'])
            area.save()
            return redirect('dashboard')
    else:
        form = AreaCreationForm()
    return render(request, 'register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            area = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=area, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

def custom_logout(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'home.html')

# Vistas para Espacios Físicos de '
#
#
# aqui pa bajo
@login_required
def lista_espacios(request):
    espacios = EspacioFisico.objects.all()
    return render(request, 'espacios/lista.html', {'espacios': espacios})

@login_required
def agregar_espacio(request):
    if request.method == 'POST':
        form = EspacioFisicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_espacios')
    else:
        form = EspacioFisicoForm()
    return render(request, 'espacios/form.html', {'form': form})

@login_required
def editar_espacio(request, pk):
    espacio = get_object_or_404(EspacioFisico, pk=pk)
    if request.method == 'POST':
        form = EspacioFisicoForm(request.POST, instance=espacio)
        if form.is_valid():
            form.save()
            return redirect('lista_espacios')
    else:
        form = EspacioFisicoForm(instance=espacio)
    return render(request, 'espacios/form.html', {'form': form})

@login_required
def eliminar_espacio(request, pk):
    espacio = get_object_or_404(EspacioFisico, pk=pk)
    espacio.delete()
    return redirect('lista_espacios')

@login_required
def lista_solicitudes(request):
    if request.user.area == "Coordinación":
        solicitudes = SolicitudEspacio.objects.filter(Q(estado=1) | Q(estado=2)| Q(estado=3))#Filtro para la lista
    elif request.user.area == "Delegación Administrativa":
        solicitudes = SolicitudEspacio.objects.filter(Q(estado=1) | Q(estado=2)| Q(estado=3))#Filtro para la lista
    else:

        solicitudes = SolicitudEspacio.objects.filter(area__area=request.user.area)


    return render(request, 'solicitudes/lista.html', {'solicitudes': solicitudes})

@login_required
def agregar_solicitud(request):
    if request.method == 'POST':
        form = SolicitudEspacioForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('lista_solicitudes')
    else:
        form = SolicitudEspacioForm(user=request.user)
    return render(request, 'solicitudes/form.html', {'form': form})

@login_required
def editar_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudEspacio, pk=pk)
    if request.method == 'POST':
        form = SolicitudEspacioForm(request.POST, instance=solicitud, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('lista_solicitudes')
    else:
        form = SolicitudEspacioForm(instance=solicitud, user=request.user)
    return render(request, 'solicitudes/form.html', {'form': form})

@login_required
def eliminar_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudEspacio, pk=pk)
    solicitud.delete()
    return redirect('lista_solicitudes')




from django.contrib import messages
@login_required
def detalle_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudEspacio, pk=pk)

    # Cambio de estado según el rol del usuario y el estado actual de la solicitud
    if request.method == "POST":
        if request.user.area == "Coordinación" and solicitud.estado == 1:
            solicitud.estado = 2
            solicitud.save()
            messages.success(request, "El estado de la solicitud se cambió.")
        elif request.user.area == "Delegación Administrativa" and solicitud.estado == 2:
            solicitud.estado = 3
            solicitud.save()
            messages.success(request, "El estado de la solicitud se cambió .")
        else:
            messages.error(request, "No tienes permisos para realizar esta acción.")

        return redirect('detalle_solicitud', pk=solicitud.pk)

    return render(request, 'solicitudes/detalle.html', {'solicitud': solicitud})





from django.http import JsonResponse
from .models import SolicitudEspacio
from django.core.serializers import serialize
@login_required
def obtener_solicitudes(request):
    solicitudes = SolicitudEspacio.objects.all()
    eventos = []

    for solicitud in solicitudes:
        eventos.append({
            "id": solicitud.pk,  # Incluye el ID de la solicitud
            "title": f"{solicitud.espacio_prestamo} ({solicitud.nombre})",
            "start": f"{solicitud.fecha}T{solicitud.hora_inicio}",  # Formato ISO 8601
            "end": f"{solicitud.fecha}T{solicitud.hora_fin}",
            "description": solicitud.otras_especificaciones,
            "estado": solicitud.get_estado_display(),
        })

    return JsonResponse(eventos, safe=False)

@login_required
def calendario_solicitudes(request):
    return render(request, 'calendario/calendar.html')


#--------------------------------------------------------------------------AGREGADOS PARA VER USUARIOS 24/02/25#

@login_required
def lista_usuarios(request):
    if request.user.area != "Coordinación":
        return redirect('dashboard')  # Solo Coordinación puede ver la lista de usuarios

    usuarios = Area.objects.all()
    return render(request, 'lista.html', {'usuarios': usuarios})




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Area
from .forms import UsuarioForm

@login_required
def editar_usuario(request, usuario_id):
    if request.user.area != "Coordinación":
        return redirect('dashboard')  # Restringir acceso

    usuario = get_object_or_404(Area, id=usuario_id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')  # Redirigir a la lista tras guardar
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'editar.html', {'form': form, 'usuario': usuario})



from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

@login_required
def cambiar_contraseña(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Evita que cierre la sesión
            return redirect('dashboard')  # Puedes redirigir a donde prefieras
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'cambiar_contraseña.html', {'form': form})

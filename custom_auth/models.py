from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.utils.timezone import now

class AreaManager(BaseUserManager):
    def create_user(self, area, password=None, **extra_fields):
        if not area:
            raise ValueError("El área es obligatoria.")
        user = self.model(area=area, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, area, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(area, password, **extra_fields)


class Area(AbstractBaseUser):
    area = models.CharField(max_length=100, unique=True)
    responsable = models.CharField(max_length=100)
    extension = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AreaManager()

    USERNAME_FIELD = 'area'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.area


class EspacioFisico(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)  # Activo o Inactivo

    def __str__(self):
        return self.nombre


class SolicitudEspacio(models.Model):
    folio = models.CharField(max_length=20, unique=True)
    fecha_solicitud = models.DateTimeField(default=now)  # Campo que se llena automáticamente con la fecha actual
    area = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100)
    extension = models.CharField(max_length=10, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    espacio_prestamo = models.ForeignKey(EspacioFisico, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    otras_especificaciones = models.TextField(blank=True, null=True)
    tipo_actividad = models.CharField(max_length=100)
    requiere_costo = models.BooleanField(default=False)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    con_cargo_a = models.CharField(max_length=100, blank=True, null=True)
    estado = models.IntegerField(choices=[(1, "Pendiente"), (2, "Aprobado"), (3, "Finalizado")], default=1)

    def __str__(self):
        return f"{self.folio} - {self.nombre}"

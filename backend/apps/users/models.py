from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from apps.sucursales.models import Sucursal


class UserManager(BaseUserManager):
    def create_user(self, usuario, password=None, **extra_fields):
        if not usuario:
            raise ValueError("El usuario es obligatorio")

        user = self.model(usuario=usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser debe tener is_superuser=True.")

        from .models import Rol

        rol_admin, _ = Rol.objects.get_or_create(nombre="admin")
        extra_fields["id_rol"] = rol_admin

        from apps.sucursales.models import Sucursal

        sucursal_default, _ = Sucursal.objects.get_or_create(
            nombre_sucursal="Principal", defaults={"direccion": "Dirección Principal", "telefono": "123456789"}
        )
        extra_fields["id_sucursal"] = sucursal_default

        return self.create_user(usuario, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):

    # Campos de database
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100, unique=True)
    id_rol = models.ForeignKey("Rol", on_delete=models.CASCADE)
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    # Campos requeridos por django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "usuario"
    REQUIRED_FIELDS = ["nombre", "apellido"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "usuario"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"

    def is_admin(self):
        return self.id_rol.nombre == "admin"

    def is_cajero(self):
        return self.id_rol.nombre == "cajero"

    def is_mesero(self):
        return self.id_rol.nombre == "mesero"


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        db_table = "rol"

    def __str__(self):
        return self.nombre

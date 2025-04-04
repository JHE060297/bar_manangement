from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class UsernameAuthenticationBackend(ModelBackend):
    """
    Autenticación basada en el campo 'usuario' en lugar de 'username'
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Para compatibilidad con SimpleJWT, que usa 'username' por defecto
        if username is not None:
            kwargs = {"usuario": username}

        # Este es el caso estándar de autenticación
        usuario = kwargs.get("usuario")
        if usuario is None:
            return None

        try:
            user = User.objects.get(usuario=usuario)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

        return None

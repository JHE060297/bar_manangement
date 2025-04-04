from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SucursalViewSet, MesaViewSet

router = DefaultRouter()
router.register(r"sucursales", SucursalViewSet)
router.register(r"mesas", MesaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

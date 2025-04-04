from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, InventarioViewSet, TransaccionInventarioViewSet

router = DefaultRouter()
router.register(r"productos", ProductoViewSet)
router.register(r"inventario", InventarioViewSet)
router.register(r"transacciones", TransaccionInventarioViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

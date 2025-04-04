from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet, DetallePedidoViewSet, PedidoMeseroViewSet, PagoViewSet

router = DefaultRouter()
router.register(r"pedidos", PedidoViewSet)
router.register(r"detalles", DetallePedidoViewSet)
router.register(r"asignaciones", PedidoMeseroViewSet)
router.register(r"pagos", PagoViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

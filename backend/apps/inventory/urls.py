from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, InventoryViewSet, InventoryTransactionViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)
router.register(r"inventory", InventoryViewSet)
router.register(r"transactions", InventoryTransactionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

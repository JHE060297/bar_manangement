from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BranchViewSet, TableViewSet

router = DefaultRouter()
router.register(r"branches", BranchViewSet)
router.register(r"tables", TableViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

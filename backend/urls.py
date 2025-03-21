from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# Créer un routeur
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

# Liste des URLs
urlpatterns = [
    # Inclure les URLs générées par le routeur
    path('', include(router.urls)),
]
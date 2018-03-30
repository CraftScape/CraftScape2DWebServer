from django.urls import path, include
from rest_framework import routers
from CraftScapeAPI import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'character', views.CharacterViewSet)

urlpatterns = [
    path('', include(router.urls))
]

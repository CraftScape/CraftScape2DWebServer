from django.contrib.auth.models import User
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from CraftScapeDatabase.models import Character, Inventory
from CraftScapeAPI.serializers import UserSerializer, CharacterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()


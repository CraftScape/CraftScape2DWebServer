from django.contrib.auth.models import User
from rest_framework import viewsets
from CraftScapeAPI.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def update(self, request, pk=None, **kwargs):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

from django.contrib.auth.models import User
from rest_framework import serializers
from CraftScapeDatabase.models import Character, Inventory, InventoryGameItem, GameItem_static


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class GameItemStatic(serializers.ModelSerializer):
    class Meta:
        model = GameItem_static
        fields = '__all__'

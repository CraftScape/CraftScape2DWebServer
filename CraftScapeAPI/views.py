from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from CraftScapeDatabase.models import Character, Inventory, GameItem, Skill, SkillDependency, CharacterSkill, \
    GameItemModifier, ItemModifier, StaticItemModifier, StaticGameItem, GameItemType, StaticItemTypeModifier, \
    Equipment
from CraftScapeAPI.serializers import UserSerializer, CharacterSerializer, InventorySerializer, GameItemSerializer, \
    SkillSerializer, SkillDependencySerializer, CharacterSkillSerializer, GameItemModifierSerializer, \
    ItemModifierSerializer, StaticItemModifierSerializer, StaticGameItemSerializer, GameItemTypeSerializer, \
    StaticItemTypeModifierSerializer, EquipmentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from operator import __or__ as OR
from functools import reduce


class BaseModelViewSet(viewsets.ModelViewSet):
    def find_all(self):
        find_all = self.request.query_params.get('find_all', '')
        return find_all.lower() == 'true'


class UserViewSet(BaseModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')

    def get_queryset(self):
        if self.request.user.is_staff and self.find_all():
            return self.queryset
        return self.queryset.filter(pk=self.request.user.pk)


class CharacterViewSet(BaseModelViewSet):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all().order_by('id')

    def get_object(self):
        character = super().get_object()
        return character

    def get_queryset(self):
        if self.request.user.is_staff and self.find_all():
            return self.queryset
        return self.queryset.filter(user=self.request.user.id)


class InventoryViewSet(BaseModelViewSet):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all().order_by('position')
    filter_fields = ('character', 'position', 'size')
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        if self.find_all() and self.request.user.is_staff:
            return self.queryset

        characters = Character.objects.filter(user=self.request.user.id)
        character_ids = [Q(character=char.id) for char in characters]
        queryset = self.queryset.filter(reduce(OR, character_ids))
        return queryset


class GameItemViewSet(viewsets.ModelViewSet):
    serializer_class = GameItemSerializer
    queryset = GameItem.objects.all()

    def create(self, request, *args, **kwargs):
        data = {
            'uuid': request.data['uuid'],
            'inventory': request.data['inventory'],
            'inventory_position': request.data['inventory_position'],
            'static_game_item_id': request.data['static_game_item']
        }
        return GameItem.objects.create(**data)


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


class SkillDependencyViewSet(viewsets.ModelViewSet):
    serializer_class = SkillDependencySerializer
    queryset = SkillDependency.objects.all()


class CharacterSkillViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSkillSerializer
    queryset = CharacterSkill.objects.all()


class GameItemModifierViewSet(viewsets.ModelViewSet):
    serializer_class = GameItemModifierSerializer
    queryset = GameItemModifier.objects.all()


class ItemModifierViewSet(viewsets.ModelViewSet):
    serializer_class = ItemModifierSerializer
    queryset = ItemModifier.objects.all()


class StaticItemModifierViewSet(viewsets.ModelViewSet):
    serializer_class = StaticItemModifierSerializer
    queryset = StaticItemModifier.objects.all()


class StaticGameItemViewSet(viewsets.ModelViewSet):
    serializer_class = StaticGameItemSerializer
    queryset = StaticGameItem.objects.all().order_by('name')


class GameItemTypeViewSet(viewsets.ModelViewSet):
    serializer_class = GameItemTypeSerializer
    queryset = GameItemType.objects.all()


class StaticItemTypeModifierViewSet(viewsets.ModelViewSet):
    serializer_class = StaticItemTypeModifierSerializer
    queryset = StaticItemTypeModifier.objects.all()


class EquipmentViewSet(BaseModelViewSet):
    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all().order_by('id')

    def get_queryset(self):
        if self.request.user.is_staff and self.find_all():
            return self.queryset

        characters = Character.objects.filter(user=self.request.user.id)
        character_ids = [Q(character=character.id) for character in characters]
        return self.queryset.filter(reduce(OR, character_ids))

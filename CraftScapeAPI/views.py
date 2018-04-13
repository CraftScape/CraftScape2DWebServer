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

    def perform_update(self, serializer):
        super().perform_update(serializer)

    def update(self, request, pk=None):
        instance = self.get_object()

        data = dict()
        for key, value in request.data.items():
            if value and key != 'id':
                data[key] = GameItem.objects.get(pk=value)
            else:
                data[key] = None

        # serializer = self.get_serializer(instance, data=data)

        if 'ring' in data:
            instance.ring = data['ring']
        else:
            data['ring'] = None
        if 'neck' in data:
            instance.neck = data['neck']
        else:
            data['neck'] = None
        if 'head' in data:
            instance.head = data['head']
        else:
            data['head'] = None
        if 'chest' in data:
            instance.chest = data['chest']
        else:
            data['chest'] = None
        if 'main_hand' in data:
            instance.main_hand = data['main_hand']
        else:
            data['main_hand'] = None
        if 'back' in data:
            instance.back = data['back']
        else:
            data['back'] = None
        if 'hands' in data:
            instance.hands = data['hands']
        else:
            data['hands'] = None
        if 'feet' in data:
            instance.feet = data['feet']
        else:
            data['feet'] = None
        if 'legs' in data:
            instance.legs = data['legs']
        else:
            data['legs'] = None

        instance.save()

        for key, value in data.items():
            if value:
                data[key] = GameItem.objects.filter(pk=value.pk).values().first()
                data[key]['static_game_item'] = StaticGameItem.objects.filter(pk=data[key]['static_game_item_id']).values().first()
                data[key]['inventory'] = data[key]['inventory_id']
                del data[key]['inventory_id']
                del data[key]['static_game_item_id']

        data['id'] = instance.pk

        return Response(data)

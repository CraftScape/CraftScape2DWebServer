from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.response import Response
from CraftScapeDatabase.models import Character, Inventory, GameItem, Skill, SkillDependency, CharacterSkill, \
    GameItemModifier, ItemModifier, StaticItemModifier, StaticGameItem, GameItemType, StaticItemTypeModifier
from CraftScapeAPI.serializers import UserSerializer, CharacterSerializer, InventorySerializer, GameItemSerializer, \
    SkillSerializer, SkillDependencySerializer, CharacterSkillSerializer, GameItemModifierSerializer, \
    ItemModifierSerializer, StaticItemModifierSerializer, StaticGameItemSerializer, GameItemTypeSerializer, \
    StaticItemTypeModifierSerializer
from django_filters.rest_framework import DjangoFilterBackend
from operator import __or__ as OR
from functools import reduce

from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        if request.data == {}:
            data = {
                'username': request.query_params.get('username', ''),
                'password': request.query_params.get('password', '')
            }
        else:
            data = request.data

        serializer = self.serializer_class(data=data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')

    def get_queryset(self):
        if self.request.user.is_staff and 'find_all' in self.request.query_params:
            return self.queryset
        return self.queryset.filter(pk=self.request.user.pk)


class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all().order_by('id')

    def get_queryset(self):
        if self.request.user.is_staff and 'find_all' in self.request.query_params:
            return self.queryset
        return self.queryset.filter(user=self.request.user.id)


class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all().order_by('position')
    filter_fields = ('character', 'position', 'size')
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        queryset = Inventory.objects.all().order_by('position')
        find_all = self.request.query_params.get('find_all', False)

        if find_all and self.request.user.is_staff:
            return queryset

        characters = Character.objects.filter(user=self.request.user.id)
        character_ids = [Q(character=char.id) for char in characters]
        queryset = queryset.filter(reduce(OR, character_ids))
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
    queryset = StaticGameItem.objects.all()


class GameItemTypeViewSet(viewsets.ModelViewSet):
    serializer_class = GameItemTypeSerializer
    queryset = GameItemType.objects.all()


class StaticItemTypeModifierViewSet(viewsets.ModelViewSet):
    serializer_class = StaticItemTypeModifierSerializer
    queryset = StaticItemTypeModifier.objects.all()



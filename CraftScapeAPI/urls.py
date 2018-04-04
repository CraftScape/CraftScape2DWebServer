from django.urls import path, include
from rest_framework import routers
from CraftScapeAPI import views
from rest_framework.authtoken import views as auth_views

router = routers.DefaultRouter()
router.register('user', views.UserViewSet, base_name='user')
router.register('character', views.CharacterViewSet, base_name='character')
router.register('inventory', views.InventoryViewSet, base_name='inventory')
router.register('game_item', views.GameItemViewSet, base_name='game_item')
router.register('skill', views.SkillViewSet, base_name='skill')
router.register('skill_dependency', views.SkillDependencyViewSet, base_name='skill_dependency')
router.register('character_skill', views.CharacterSkillViewSet, base_name='character_skill')
router.register('game_item_modifier', views.GameItemModifierViewSet, base_name='game_item_modifier')
router.register('item_modifier', views.ItemModifierViewSet, base_name='item_modifier')
router.register('static_item_modifier', views.StaticItemModifierViewSet, base_name='static_item_modifier')
router.register('static_game_item', views.StaticGameItemViewSet, base_name='static_game_item')
router.register('game_item_type', views.GameItemTypeViewSet, base_name='game_item_type')
router.register('static_item_type_modifier', views.StaticItemTypeModifierViewSet, base_name='static_item_type_modifier')

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
    path('authorize/', auth_views.obtain_auth_token)
]

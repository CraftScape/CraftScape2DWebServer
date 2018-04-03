from django.contrib.auth.models import User
from rest_framework import serializers
from CraftScapeDatabase.models import Character, Inventory, GameItem, Skill, SkillDependency, CharacterSkill, \
    GameItemModifier, ItemModifier, StaticItemModifier, StaticGameItem, GameItemType, StaticItemTypeModifier


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class SkillDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillDependency
        fields = '__all__'


class CharacterSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterSkill
        fields = '__all__'


class GameItemModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameItemModifier
        fields = '__all__'


class ItemModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModifier
        fields = '__all__'


class StaticItemModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticItemModifier
        fields = '__all__'


class StaticGameItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticGameItem
        fields = '__all__'


class GameItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameItemType
        fields = '__all__'


class StaticItemTypeModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticItemTypeModifier
        fields = '__all__'


class GameItemSerializer(serializers.ModelSerializer):
    static_game_item = StaticGameItemSerializer(many=False, read_only=True)

    class Meta:
        model = GameItem
        fields = ('id', 'url', 'inventory', 'inventory_position', 'created_by', 'created_by_name', 'static_game_item')


class InventorySerializer(serializers.ModelSerializer):
    game_items = GameItemSerializer(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = ('id', 'position', 'character', 'size', 'game_items')


class CharacterSerializer(serializers.ModelSerializer):
    inventories = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:inventory-detail')

    class Meta:
        model = Character
        fields = ('user', 'name', 'health', 'max_health', 'currency', 'walk_speed', 'inventories')


class UserSerializer(serializers.ModelSerializer):
    characters = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:character-detail')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'characters')

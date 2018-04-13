from django.contrib.auth.models import User
from rest_framework import serializers
from CraftScapeDatabase.models import Character, Inventory, GameItem, Skill, SkillDependency, CharacterSkill, \
    GameItemModifier, ItemModifier, StaticItemModifier, StaticGameItem, GameItemType, StaticItemTypeModifier, \
    Equipment


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
    item_type = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = StaticGameItem
        fields = ('id', 'name', 'sprite_name', 'description', 'max_stack', 'value', 'equipable', 'rarity', 'min_level',
                  'base_durability', 'soulbound', 'power', 'defense', 'vitality', 'heal_amount', 'item_type')


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
        fields = ('id', 'url', 'inventory', 'inventory_position', 'stack_size', 'created_by', 'created_by_name',
                  'static_game_item')

    def create(self, validated_data):
        static_game_item_id = self.context['request'].data['static_game_item']
        static_game_item = StaticGameItem.objects.get(pk=static_game_item_id)
        data = {
            "inventory": validated_data.pop('inventory'),
            "inventory_position": validated_data.pop('inventory_position'),
            "stack_size": validated_data.pop('stack_size'),
            "created_by": validated_data.pop("created_by"),
            "static_game_item": static_game_item
        }
        item = GameItem.objects.create(**data)
        return item


class InventorySerializer(serializers.ModelSerializer):
    game_items = GameItemSerializer(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = ('id', 'position', 'character', 'size', 'game_items')


class CharacterSerializer(serializers.ModelSerializer):
    inventories = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:inventory-detail')
    equipment = serializers.HyperlinkedRelatedField(read_only=True, view_name="api:equipment-detail")

    class Meta:
        model = Character
        fields = ('id', 'user', 'name', 'health', 'max_health', 'currency', 'walk_speed', 'inventories', 'equipment')


class UserSerializer(serializers.ModelSerializer):
    characters = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:character-detail')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'characters')


class EquipmentSerializer(serializers.ModelSerializer):
    ring = GameItemSerializer()
    neck = GameItemSerializer(many=False)
    head = GameItemSerializer(many=False)
    chest = GameItemSerializer(many=False)
    weapon = GameItemSerializer(many=False)
    back = GameItemSerializer(many=False)
    hands = GameItemSerializer(many=False)
    feet = GameItemSerializer(many=False)
    legs = GameItemSerializer(many=False)

    class Meta:
        model = Equipment
        fields = ('id', 'ring', 'neck', 'head', 'chest', 'weapon', 'back', 'hands', 'feet', 'legs')

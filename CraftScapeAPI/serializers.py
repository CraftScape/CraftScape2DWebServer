import uuid
from django.contrib.auth.models import User
from django.db.models import ManyToOneRel
from rest_framework import serializers
from CraftScapeDatabase.models import Character, Inventory, GameItem, Skill, SkillDependency, CharacterSkill, \
    GameItemModifier, ItemModifier, StaticItemModifier, StaticGameItem, GameItemType, StaticItemTypeModifier, \
    Equipment, Ingredient


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
    item_types = serializers.StringRelatedField(many=True, read_only=True)

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
    created_by_name = serializers.ReadOnlyField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GameItem
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': True,
                'required': False
            },
            'inventory_position': {
                'required': False
            }
        }

    def create(self, validated_data):
        static_game_item_id = self.context['request'].data['static_game_item']
        static_game_item = StaticGameItem.objects.get(pk=static_game_item_id)
        inventory = Inventory.objects.get(pk=self.context['request'].data['inventory'])
        created_by = inventory.character
        data = {
            "uuid": validated_data.pop("uuid"),
            "inventory_position": validated_data.pop('inventory_position'),
            "stack_size": validated_data.pop('stack_size'),
            "inventory": inventory,
            "created_by": created_by,
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
        fields = ('id', 'user', 'name', 'health', 'max_health', 'currency', 'walk_speed', 'inventories', 'equipment', 'experience')


class UserSerializer(serializers.ModelSerializer):
    characters = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:character-detail')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'characters')


class EquipmentSerializer(serializers.ModelSerializer):
    ring = GameItemSerializer(required=False, allow_null=True)
    neck = GameItemSerializer(required=False, allow_null=True)
    head = GameItemSerializer(required=False, allow_null=True)
    shoulders = GameItemSerializer(required=False, allow_null=True)
    chest = GameItemSerializer(required=False, allow_null=True)
    main_hand = GameItemSerializer(required=False, allow_null=True)
    back = GameItemSerializer(required=False, allow_null=True)
    hands = GameItemSerializer(required=False, allow_null=True)
    feet = GameItemSerializer(required=False, allow_null=True)
    legs = GameItemSerializer(required=False, allow_null=True)

    class Meta:
        model = Equipment
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': True
            }
        }

    def update(self, instance, validated_data):
        field_names = list()
        for field in Equipment._meta.get_fields():
            if not isinstance(field, ManyToOneRel) and field.name != 'id':
                field_names.append(field.name)

        for name in field_names:
            if name in validated_data and validated_data[name] is not None:
                setattr(instance, name, GameItem.objects.get(uuid=validated_data[name]['uuid']))
            else:
                setattr(instance, name, None)

        instance.save()

        return instance


class IngredientSerializer(serializers.ModelSerializer):
    static_game_item = StaticGameItemSerializer(many=False, read_only=True)
    
    class Meta:
        model = Ingredient
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    static_game_item = StaticGameItemSerializer(many=False, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    
    class Meta:
        model = Skill
        fields = '__all__'


class SkillDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillDependency
        fields = '__all__'


class CharacterSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=False, read_only=True)
    
    class Meta:
        model = CharacterSkill
        fields = '__all__'
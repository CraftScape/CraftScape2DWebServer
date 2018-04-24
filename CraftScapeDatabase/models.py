import uuid
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=255)
    health = models.FloatField(default=100)
    max_health = models.FloatField(default=100)
    currency = models.IntegerField(default=0)
    walk_speed = models.FloatField(default=10)
    max_inventories = models.IntegerField(default=5)
    equipment = models.OneToOneField('Equipment', on_delete=models.CASCADE, related_name='character')
    x_pos = models.FloatField(blank=True, null=True)
    y_pos = models.FloatField(blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        inventory = None
        if not self.pk:
            equipment = Equipment()
            equipment.save()
            self.equipment = equipment

            inventory = Inventory(position=0, size=16)

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        if inventory:
            inventory.character = self
            inventory.save()

    def delete(self, using=None, keep_parents=False):
        raise MethodNotAllowed('Characters may not be deleted once created')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'character'


class CharacterSkill(models.Model):
    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)

    def __str__(self):
        return "{0} : {1}".format(self.character, self.skill)

    class Meta:
        db_table = 'character_skill'


class Skill(models.Model):
    name = models.CharField(max_length=30)
    skill_type = models.CharField(max_length=30)
    value = models.FloatField()
    static_game_item = models.ForeignKey('StaticGameItem', on_delete=models.CASCADE, related_name='skill')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'skill'


class SkillDependency(models.Model):
    child_skill = models.ForeignKey('Skill', on_delete=models.CASCADE, related_name="childSkill", )
    parent_skill = models.ForeignKey('Skill', on_delete=models.CASCADE, related_name="parentSkill", )

    UNION = "U"  # Gaining any child skill unlocks the parent skill.
    INTERSECTION = "I"  # Gaining all child skills unlocks the parent skill.

    DEPENDENCY_TYPES = (
        (UNION, "union"),
        (INTERSECTION, "intersection"),
    )

    dependency_type = models.CharField(max_length=1, choices=DEPENDENCY_TYPES, default=UNION)

    def __str__(self):
        return self.child_skill.__str__() + " depends on " + self.parent_skill.__str__() + " (" + self.dependency_type + ")"

    class Meta:
        db_table = 'skill_dependency'


class Inventory(models.Model):
    SMALL = 'SM'
    MEDIUM = 'MD'
    LARGE = 'LG'

    INVENTORY_SIZES = {
        'SM': 8,
        'MD': 12,
        'LG': 16
    }

    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='inventories')
    position = models.IntegerField(default=-1)
    size = models.IntegerField(default=INVENTORY_SIZES[SMALL])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id is None or self.position < 0 or not self.position_is_available():
            self.position = self.get_next_position()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def get_available_positions(self):
        return [inv.position for inv in Inventory.objects.filter(character=self.character.id)]

    def get_next_position(self):
        curr_positions = self.get_available_positions()
        remaining_pos = list(filter(lambda x: x not in curr_positions, list(range(1, self.character.max_inventories + 1))))
        if len(remaining_pos) == 0:
            raise Exception('maximum inventories reached.')
        return remaining_pos[0]

    def position_is_available(self):
        return self.position not in [inv.position for inv in Inventory.objects.filter(character=self.character.id)]

    def __str__(self):
        return "<Inventory<Owner: {}, pos: {}>>".format(self.character.name, self.position)

    def __unicode__(self):
        return 'inventory'

    class Meta:
        db_table = 'inventory'


class StaticGameItem(models.Model):
    COMMON = 1
    RARE = 2
    LEGENDARY = 3

    RARITIES = (
        (COMMON, 'Common'),
        (RARE, 'Rare'),
        (LEGENDARY, 'Legendary'),
    )

    name = models.CharField(max_length=30)
    sprite_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    max_stack = models.IntegerField()
    value = models.FloatField()
    equipable = models.BooleanField()
    rarity = models.IntegerField(choices=RARITIES, default=COMMON)
    min_level = models.IntegerField(default=1)
    base_durability = models.IntegerField(default=1)
    soulbound = models.BooleanField(default=False)
    power = models.FloatField(default=0)
    defense = models.FloatField(default=0)
    vitality = models.FloatField(default=0)
    heal_amount = models.FloatField(default=0)
    item_types = models.ManyToManyField('GameItemType', related_name='static_game_item')

    @property
    def item_type(self):
        return 'NA'

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'static_game_item'


class GameItem(models.Model):
    """
        Game Item
    """
    uuid = models.UUIDField(verbose_name='uuid', default=uuid.uuid4)
    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, related_name='game_items', null=True, blank=True)
    static_game_item = models.ForeignKey(StaticGameItem, on_delete=models.SET_NULL, related_name='static_game_item', null=True)
    created_by = models.ForeignKey(Character, on_delete=models.SET_NULL, related_name='created_by', blank=True, null=True)
    inventory_position = models.IntegerField()
    stack_size = models.IntegerField(default=1)

    @property
    def types(self):
        sgi = StaticGameItem.objects.get(pk=self.static_game_item.pk)
        item_types = sgi.item_types.all()
        return [t.item_type for t in item_types]

    @property
    def name(self):
        return self.static_game_item.name

    @property
    def created_by_name(self):
        return self.created_by.name if self.created_by else None

    @property
    def url(self):
        url = reverse('api:game_item-detail', kwargs={'pk': self.pk})
        return "{base_url}{url}".format(base_url=settings.BASE_URL, url=url)

    def __str__(self):
        return self.inventory.__str__() + ": " + self.static_game_item.__str__()

    def clean(self):
        super().clean()
        if self.stack_size > self.static_game_item.max_stack:
            raise ValidationError('Stack size has exceeded the max stack size.')

    class Meta:
        db_table = 'game_item'


class GameItemType(models.Model):
    """
    Item Types
    """
    item_type = models.CharField(max_length=255)

    def __str__(self):
        return self.item_type

    class Meta:
        db_table = 'game_item_type'


class GameItemModifier(models.Model):
    game_item = models.ForeignKey('GameItem', on_delete=models.CASCADE)
    modifier = models.ForeignKey('ItemModifier', on_delete=models.CASCADE)

    def __str__(self):
        return self.game_item.__str__() + ": " + self.inventory_modifier.__str__()

    class Meta:
        db_table = 'game_item__item_modifier'


class ItemModifier(models.Model):
    item_modifier = models.ForeignKey('StaticItemModifier', on_delete=models.CASCADE)
    duration_remainder = models.IntegerField()  # in seconds
    modifier_remainder = models.FloatField()

    def __str__(self):
        return self.item_modifier.__str__()

    class Meta:
        db_table = 'item_modifier'


class StaticItemModifier(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    modifier = models.FloatField()
    duration = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'item_modifier_static'


class StaticItemTypeModifier(models.Model):
    item_type_id = models.ForeignKey('StaticGameItem', on_delete=models.CASCADE)
    item_modifier_id = models.ForeignKey('StaticItemModifier', on_delete=models.CASCADE)

    def __str__(self):
        return self.item_modifier_id.__str__() + " can effect " + self.item_type_id.__str__()

    class Meta:
        db_table = 'static_item_type_modifier'


class Equipment(models.Model):
    ring = models.ForeignKey(GameItem, on_delete=models.SET_NULL, related_name='ring', null=True, blank=True)
    neck = models.ForeignKey(GameItem, on_delete=models.SET_NULL, related_name='neck', null=True, blank=True)
    head = models.ForeignKey(GameItem, on_delete=models.SET_NULL, related_name='head', null=True, blank=True)
    shoulders = models.ForeignKey(GameItem, on_delete=models.SET_NULL, related_name='shoulders', null=True, blank=True)
    chest = models.ForeignKey(GameItem, on_delete=models.SET_NULL, related_name='chest', null=True, blank=True)
    main_hand = models.ForeignKey(GameItem, on_delete=models.SET_NULL, related_name='main_hand', null=True, blank=True)
    back = models.ForeignKey(GameItem, on_delete=models.SET_NULL, related_name='back', null=True, blank=True)
    hands = models.ForeignKey(GameItem, on_delete=models.SET_NULL, related_name='hands', null=True, blank=True)
    feet = models.ForeignKey(GameItem, on_delete=models.SET_NULL, related_name='feet', null=True, blank=True)
    legs = models.ForeignKey(GameItem, on_delete=models.SET_NULL, related_name='legs', null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.ring and 'ring' not in self.ring.types:
            raise serializers.ValidationError("Cannot equip {0} in ring slot".format(self.ring.name))
        if self.neck and 'neck' not in self.neck.types:
            raise serializers.ValidationError("Cannot equip {0} in neck slot".format(self.neck.name))
        if self.head and 'head' not in self.head.types:
            raise serializers.ValidationError("Cannot equip {0} in head slot".format(self.head.name))
        if self.shoulders and 'shoulders' not in self.shoulders.types:
            raise serializers.ValidationError("Cannot equip {0} in shoulders slot".format(self.head.name))
        if self.chest and 'chest' not in self.chest.types:
            raise serializers.ValidationError("Cannot equip {0} in chest slot".format(self.chest.name))
        if self.main_hand and 'mainHand' not in self.main_hand.types:
            raise serializers.ValidationError("Cannot equip {0} in main_hand slot".format(self.main_hand.name))
        if self.back and 'back' not in self.back.types:
            raise serializers.ValidationError("Cannot equip {0} in back slot".format(self.back.name))
        if self.hands and 'hands' not in self.hands.types:
            raise serializers.ValidationError("Cannot equip {0} in hands slot".format(self.hands.name))
        if self.feet and 'feet' not in self.feet.types:
            raise serializers.ValidationError("Cannot equip {0} in feet slot".format(self.feet.name))
        if self.legs and 'legs' not in self.legs.types:
            raise serializers.ValidationError("Cannot equip {0} in legs slot".format(self.legs.name))
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        try:
            name = Character.objects.get(equipment=self.id).name
        except:
            name = 'NA'
        return '<Equipment <Owner: {0}>>'.format(name)

    class Meta:
        db_table = 'equipment'

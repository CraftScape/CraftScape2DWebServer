from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import escape
from django.shortcuts import reverse
from django.conf import settings
from django.core.exceptions import ValidationError


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=255)
    health = models.FloatField(default=100)
    max_health = models.FloatField(default=100)
    currency = models.IntegerField(default=0)
    walk_speed = models.FloatField(default=10)
    max_inventories = models.IntegerField(default=5)

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
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

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

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'static_game_item'


class GameItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='game_items')
    static_game_item = models.ForeignKey(StaticGameItem, on_delete=models.CASCADE, related_name='static_game_item')
    created_by = models.ForeignKey(Character, on_delete=models.SET_NULL, related_name='created_by', blank=True, null=True)
    inventory_position = models.IntegerField()
    stack_size = models.IntegerField(default=1)

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


class GameItemType(models.Model):
    static_game_item = models.ForeignKey(StaticGameItem, on_delete=models.PROTECT, related_name='item_type')
    item_type = models.CharField(max_length=255)

    def __str__(self):
        return self.item_type

    class Meta:
        db_table = 'game_item_type'


class StaticItemTypeModifier(models.Model):
    item_type_id = models.ForeignKey('StaticGameItem', on_delete=models.CASCADE)
    item_modifier_id = models.ForeignKey('StaticItemModifier', on_delete=models.CASCADE)

    def __str__(self):
        return self.item_modifier_id.__str__() + " can effect " + self.item_type_id.__str__()

    class Meta:
        db_table = 'static_item_type_modifier'

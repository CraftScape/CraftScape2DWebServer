from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=35)

    def __str__(self):
        return self.email
class Character(models.Model):
    user_id = models.ForeignKey(
        'User',
        on_delete = models.CASCADE,
    )
    screen_name = models.CharField(max_length=255)
    health = models.FloatField()
    max_health = models.FloatField()
    currency = models.IntegerField()
    walk_speed = models.FloatField()
    max_inventories = models.IntegerField()
    inventory_1_id = models.ForeignKey(
        'Inventory',
        on_delete = models.SET_NULL,
        related_name = 'inventory1',
        null = True,
    )
    inventory_2_id = models.ForeignKey(
        'Inventory',
        on_delete = models.SET_NULL,
        related_name = 'inventory2',
        null = True,
    )
    inventory_3_id = models.ForeignKey(
        'Inventory',
        on_delete = models.SET_NULL,
        related_name = 'inventory3',
        null = True,
    )
    inventory_4_id = models.ForeignKey(
        'Inventory',
        on_delete = models.SET_NULL,
        related_name = 'inventory4',
        null = True,
    )
    inventory_5_id = models.ForeignKey(
        'Inventory',
        on_delete = models.SET_NULL,
        related_name = 'inventory5',
        null = True,
    )

    def __str__(self):
        return self.screen_name
    

class Character_Skill(models.Model):
    char_id = models.ForeignKey(
        'Character',
        on_delete = models.CASCADE,
    )
    skill_id = models.ForeignKey(
        'Skill',
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return self.char_id + ": " + self.skill_id

class Skill(models.Model):
    name = models.CharField(max_length=30)
    skill_type = models.CharField(max_length=30)
    value = models.FloatField()

    def __str__(self):
        return self.name

class Skill_SkillDependency(models.Model):
    child_skill = models.ForeignKey(
        'Skill',
        on_delete = models.CASCADE,
        related_name = "childSkill",
    )
    parent_skill = models.ForeignKey(
        'Skill',
        on_delete = models.CASCADE,
        related_name = "parentSkill",
    )

    UNION = "U" # Gaining any child skill unlocks the parent skill.
    INTERSECTION = "I" # Gaining all child skills unlocks the parent skill.

    DEPENDENCY_TYPES = (
        (UNION, "union"),
        (INTERSECTION, "intersection"),
    )

    dependency_type = models.CharField(
        max_length = 1,
        choices = DEPENDENCY_TYPES,
        default = UNION,
    )

    def __str__(self):
        return self.child_skill.__str__() + " depends on " + self.parent_skill.__str__() + " (" + self.dependency_type + ")"

class Inventory(models.Model):
    character_id = models.ForeignKey(
        'Character',
        on_delete = models.CASCADE,
    )
    inventory_size = models.IntegerField()

    DEFAULT = 'DE'
    SMALLBAG = 'SB'
    MEDIUMBAG = 'MB'
    LARGEBAG = 'LB'

    INVENTORY_TYPES = (
        (DEFAULT, 'default'),
        (SMALLBAG, 'smallBag'),
        (MEDIUMBAG, 'mediumBag'),
        (LARGEBAG, 'largeBag'),
    )
    inventory_type = models.CharField(
        max_length = 2,
        choices = INVENTORY_TYPES,
        default = DEFAULT,
    )
    #This should create a kind of enumeration. There's no number associated with each option,
    #but there are a limited number of options.

    def __str__(self):
        return self.inventory_type

class Inventory_GameItem(models.Model):
    inventory_id = models.ForeignKey(
        'Inventory',
        on_delete = models.CASCADE,
    )
    game_item_id = models.ForeignKey(
        'GameItem_static',
        on_delete = models.CASCADE,
    )
    crafted_by = models.ForeignKey(
        'Character',
        on_delete = models.SET_NULL,
        null = True,
    )

    def __str__(self):
        return self.inventory_id.__str__() + ": " + self.game_item_id.__str__()

class InventoryGameItem_ItemModifier(models.Model):
    inventory_game_item_id = models.ForeignKey(
        'Inventory_GameItem',
        on_delete = models.CASCADE,
    )
    inventory_modifier_id = models.ForeignKey(
        'ItemModifier',
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return self.inventory_game_item_id.__str__() + ": " + self.inventory_modifier_id.__str__()

class ItemModifier(models.Model):
    item_modifier_id = models.ForeignKey(
        'ItemModifier_static',
        on_delete = models.CASCADE,
    )
    duration_remainder = models.IntegerField()
    modifier_remainder = models.FloatField()

    def __str__(self):
        return self.item_modifier_id.__str__()

class ItemModifier_static(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    modifier = models.FloatField()
    duration = models.IntegerField()

    def __str__(self):
        return self.name

class GameItem_static(models.Model):
    name = models.CharField(max_length=30)
    item_type = models.ForeignKey(
        'ItemType_static',
        on_delete = models.CASCADE,
        related_name = 'itemType',
    )
    max_stack = models.IntegerField()
    value = models.FloatField()

    COMMON = 1
    RARE = 2
    LEGENDARY = 3

    RARITIES = (
        (COMMON, 'Common'),
        (RARE, 'Rare'),
        (LEGENDARY, 'Legendary'),
    )

    rarity = models.IntegerField(
        choices = RARITIES,
        default = COMMON,
    )
    
    min_level = models.IntegerField()
    base_durability = models.IntegerField()
    soulbound = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ItemType_static(models.Model):
    item_type = models.CharField(max_length=30)

    def __str__(self):
        return self.item_type

class ItemModifier_can_effect_ItemType_static(models.Model):
    item_type_id = models.ForeignKey(
        'ItemType_static',
        on_delete = models.CASCADE,
    )
    item_modifier_id = models.ForeignKey(
        'ItemModifier_static',
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return self.item_modifier_id.__str__() + " can effect " + self.item_type_id.__str__()
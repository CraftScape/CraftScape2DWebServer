from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=35)
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
        on_delete = models.SET_DEFAULT
    )
    inventory_2_id = models.ForeignKey(
        'Inventory',
        on_delete = models.SET_DEFAULT
    )
    inventory_3_id = models.ForeignKey(
        'Inventory',
        on_delete = models.SET_DEFAULT
    )
    inventory_4_id = models.ForeignKey(
        'Inventory',
        on_delete = models.SET_DEFAULT
    )
    inventory_5_id = models.ForeignKey(
        'Inventory',
        on_delete = models.SET_DEFAULT
    )
    

class Character_Skill(models.Model):
    char_id = models.ForeignKey(
        'Character',
        on_delete = models.CASCADE,
    )
    skill_id = models.ForeignKey(
        'Skill',
        on_delete = models.CASCADE,
    )

class Skill(models.Model):
    name = models.CharField()
    skill_type = models.CharField()
    value = models.FloatField()

class Skill_SkillDependency(models.Model):
    child_skill = models.ForeignKey(
        'Skill',
        on_delete = models.CASCADE,
    )
    parent_skill = models.ForeignKey(
        'Skill',
        on_delete = models.CASCADE,
    )

class Inventory(models.Model):
    character_id = models.ForeignKey(
        'Character',
        on_delete = models.CASCADE,
    )
    inventory_size = models.IntegerField()
    INVENTORY_TYPES = model.Choices('default', 'smallBag', 'mediumBag', 'largeBag')
    inventory_type = model.StatusField(choices_name = 'INVENTORY_TYPES')
    #This should create a kind of enumeration. There's no number associated with each option,
    #but there are a limited number of options.

class Inventory_GameItem(models.Model):
    inventory_id = models.ForeignKey(
        'Inventory',
        on_delete = models.CASCADE,
    )
    game_item_id = models.ForeignKey(
        'GameItem__static',
        on_delete = models.CASCADE,
    )
    crafted_by = models.ForeignKey(
        'Character',
        on_delete = models.SET_DEFAULT,
    )

class InventoryGameItem_ItemModifier(models.Model):
    inventory_game_item_id = models.ForeignKey(
        'Inventory_GameItem',
        on_delete = models.CASCADE,
    )
    inventory_modifier_id = models.ForeignKey(
        'ItemModifier',
        on_delete = models.CASCADE,
    )

class ItemModifier(models.Model):
    item_modifier_id = models.ForeignKey(
        'ItemModifier__static',
        on_delete = models.CASCADE,
    )
    duration_remainder = models.IntegerField()
    modifier_remainder = models.FloatField()

class ItemModifier__static(models.Model):
    name = models.CharField()
    description = models.CharField()
    modifier = models.FloatField()
    duration = models.IntegerField()

class GameItem__static(models.Model):
    name = models.CharField()
    item_type = models.ForeignKey(
        'ItemType__static',
        on_delete = models.CASCADE,
    )
    max_stack = models.IntegerField()
    value = models.FloatField()
    RARITIES = models.Choices('common', 'rare', 'legendary')
    rarity = model.StatusField(choices_name = 'RARITIES')
    #This should create a kind of enumeration. There's no number associated with each option,
    #but there are a limited number of options.
    
    min_level = models.IntegerField()
    base_durability = models.IntegerField()
    soulbound = models.BooleanField(default=False)

class ItemType__static(models.Model):
    item_type = models.CharField()
    game_item_id = models.ForeignKey(
        'GameItem__static',
        on_delete = models.CASCADE,
    )

class ItemModifier__can_effect__ItemType__static(models.Model):
    item_type_id = models.ForeignKey(
        'ItemType__static',
        on_delete = models.CASCADE,
    )
    item_modifier_id = models.ForeignKey(
        'ItemModifier__static',
        on_delete = models.CASCADE,
    )
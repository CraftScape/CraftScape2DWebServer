from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Character)
admin.site.register(CharacterSkill)
admin.site.register(Skill)
admin.site.register(SkillSkillDependency)
admin.site.register(Inventory)
admin.site.register(InventoryGameItem)
admin.site.register(InventoryGameItem_ItemModifier)
admin.site.register(ItemModifier)
admin.site.register(ItemModifier_static)
admin.site.register(GameItem_static)
admin.site.register(ItemType_static)
admin.site.register(ItemModifier_can_effect_ItemType_static)
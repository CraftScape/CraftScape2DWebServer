from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Character)
admin.site.register(Character_Skill)
admin.site.register(Skill)
admin.site.register(Skill_SkillDependency)
admin.site.register(Inventory)
admin.site.register(Inventory_GameItem)
admin.site.register(InventoryGameItem_ItemModifier)
admin.site.register(ItemModifier)
admin.site.register(ItemModifier_static)
admin.site.register(GameItem_static)
admin.site.register(ItemType_static)
admin.site.register(ItemModifier_can_effect_ItemType_static)
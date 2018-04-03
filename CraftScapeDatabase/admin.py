from django.contrib import admin

from CraftScapeDatabase.models import Character, Inventory, GameItem, Skill, SkillDependency, CharacterSkill, \
    GameItemModifier, ItemModifier, StaticItemModifier, StaticGameItem, GameItemType, StaticItemTypeModifier

admin.register(Inventory)
admin.site.register(Character)
admin.site.register(GameItem)
admin.site.register(Inventory)
admin.site.register(StaticGameItem)
admin.site.register(Skill)
admin.site.register(SkillDependency)
admin.site.register(CharacterSkill)
admin.site.register(GameItemModifier)
admin.site.register(ItemModifier)
admin.site.register(StaticItemModifier)
admin.site.register(GameItemType)
admin.site.register(StaticItemTypeModifier)

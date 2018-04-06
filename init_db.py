# from django.contrib.auth.models import User
from CraftScapeDatabase.models import StaticGameItem


def save_static_item(item):
    items = StaticGameItem.objects.filter(name=item.name)
    if len(items) == 0:
        item.save()


apple = StaticGameItem(name='apple',
                       sprite_name='apple',
                       description='An apple.',
                       max_stack=10,
                       value=5.0,
                       rarity=1,
                       base_durability=0,
                       soulbound=False,
                       power=0,
                       defense=0,
                       vitality=0,
                       heal_amount=10.0)
save_static_item(apple)

axe = StaticGameItem(name='axe',
                     sprite_name='axe',
                     description='An axe.',
                     max_stack=1,
                     value=15.0,
                     rarity=1,
                     base_durability=10,
                     soulbound=True,
                     power=10,
                     defense=5,
                     vitality=5,
                     heal_amount=0)
save_static_item(axe)

bag = StaticGameItem(name='bag',
                     sprite_name='bag',
                     description='A bag.',
                     max_stack=1,
                     value=10.0,
                     rarity=1,
                     base_durability=0,
                     soulbound=True,
                     power=0,
                     defense=0,
                     vitality=0,
                     heal_amount=0)
save_static_item(bag)

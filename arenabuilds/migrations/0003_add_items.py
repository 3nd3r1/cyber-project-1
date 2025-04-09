# Generated by Django 5.1.7 on 2025-04-09 07:40

import json

import requests
from django.db import migrations


def get_items():
    url = "https://ddragon.leagueoflegends.com/cdn/15.7.1/data/en_US/item.json"

    r = requests.get(url)
    data = json.loads(r.text)
    used_names = set()

    items = []
    for key, item in data["data"].items():
        if item["name"] not in used_names:
            used_names.add(item["name"])
            items.append(
                {
                    "name": item["name"],
                    "icon_url": f"https://ddragon.leagueoflegends.com/cdn/15.7.1/img/item/{key}.png",
                }
            )

    return items


def add_items(apps, schema_editor):
    Item = apps.get_model("arenabuilds", "Item")

    for item in get_items():
        Item.objects.create(name=item["name"], icon_url=item["icon_url"])


def remove_items(apps, schema_editor):
    Item = apps.get_model("arenabuilds", "Item")
    Item.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("arenabuilds", "0002_add_champion"),
    ]

    operations = [
        migrations.RunPython(add_items, remove_items),
    ]

from django.contrib import admin
from .models import Build, Champion, Item, Augment, BuildItem, BuildAugment

# Register all models
admin.site.register(Build)
admin.site.register(Champion)
admin.site.register(Item)
admin.site.register(Augment)
admin.site.register(BuildItem)
admin.site.register(BuildAugment)

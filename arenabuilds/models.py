from django.contrib.auth.models import User
from django.db import models


class Champion(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to="champions/", null=True, blank=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to="items/", null=True, blank=True)

    def __str__(self):
        return self.name


class Augment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to="augments/", null=True, blank=True)

    def __str__(self):
        return self.name


class Build(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    description = models.TextField()

    items = models.ManyToManyField(Item, through="BuildItem")
    augments = models.ManyToManyField(Augment, through="BuildAugment")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.champion} - {self.title}"


class BuildItem(models.Model):
    build = models.ForeignKey(Build, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class BuildAugment(models.Model):
    build = models.ForeignKey(Build, on_delete=models.CASCADE)
    augment = models.ForeignKey(Augment, on_delete=models.CASCADE)

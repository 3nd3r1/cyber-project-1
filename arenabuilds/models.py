from django.contrib.auth.models import User
from django.db import models


class Build(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="builds")
    champion = models.CharField(max_length=100)
    description = models.TextField()
    items = models.TextField(help_text="Comma-separated list of items")
    augments = models.TextField(help_text="Comma-separated list of augments")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.champion} - {self.title}"

    class Meta:
        ordering = ["-created_at"]

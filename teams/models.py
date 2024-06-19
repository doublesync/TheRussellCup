from django.db import models


# Create your models here.
class Team(models.Model):
    # Defined fields
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    color = models.CharField(max_length=10, default="#434648")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} {self.name}"

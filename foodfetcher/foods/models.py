from django.db import models

# Create your models here.


class FavoriteFoods(models.Model):
    question = models.CharField()
    answer = models.CharField()
    foods = models.JSONField()
    veggy = models.BooleanField(default=False)

    def __str__(self):
        return self.foods
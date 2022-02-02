from django.db import models
from django.utils import timezone


class Player(models.Model):
    name = models.CharField(max_length=200)
    score = models.IntegerField(
            blank=True, null=True)
    game_end = models.DateTimeField(
            blank=True, null=True)

    def gameover(self):
        self.game_end = timezone.now()
        self.save()

    def __str__(self):
        return self.name

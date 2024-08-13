from django.db import models
from django.conf import settings

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    rating = models.FloatField()
    favorite_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_games', blank=True)
    image = models.ImageField(upload_to='game_images/', blank=True, null=True)

    def __str__(self):
        return self.title

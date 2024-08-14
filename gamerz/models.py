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
    


class GamingStation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    station = models.ForeignKey(GamingStation, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.IntegerField(default=1)  # Duration in hours

    def calculate_cost(self):
        return self.duration * 200  # Ksh 200 per hour

    def __str__(self):
        return f"{self.user.username} - {self.station.name} ({self.start_time} to {self.end_time})"


class Achievement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class GamerScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField()
    achievements = models.ManyToManyField(Achievement, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.game.title}: {self.score}"



class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"



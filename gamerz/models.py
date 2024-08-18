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



class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    max_participants = models.PositiveIntegerField()
    prize = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=0.00)
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Canceled', 'Canceled')])
    registration_fee = models.DecimalField(max_digits=6, decimal_places=2, null=True, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Registered', 'Registered'), ('Attending', 'Attending'), ('Withdrawn', 'Withdrawn')])
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')


class Membership(models.Model):
    TIER_CHOICES = [
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
        ('Elite', 'Elite'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default='Basic')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.tier}"

class MembershipPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration_days = models.IntegerField()
    benefits = models.TextField()

    def __str__(self):
        return self.name





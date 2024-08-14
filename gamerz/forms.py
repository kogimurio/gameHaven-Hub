from django import forms
from .models import Game
from .models import Event


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'genre', 'release_date', 'rating', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter game title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter game description'}),
            'genre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter game genre'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10, 'step': 0.1}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date', 'end_date', 'location', 'max_participants']





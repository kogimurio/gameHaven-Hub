from django import forms
from .models import *


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
        fields = ['name', 'description', 'start_date', 'end_date', 'location', 'max_participants', 'registration_fee']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'}),
        }




class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['tier']


class CustomSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'form-control custom-select'}
        super().__init__(*args, **kwargs)


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['date', 'client', 'total_sales']
        widgets = {
            'date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'client': CustomSelect(),  # Apply the custom widget
            'total_sales': forms.NumberInput(attrs={'class': 'form-control'}),
        }



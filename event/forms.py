from django import forms
from .models import Event

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'picture', 'description', 'venue', 'link', 'date', 'time')
    
        widgets = {
            'title': forms.Textarea(attrs={
                'id': 'new-journal-title',
                'autofocus': True,
            }),
            'sub_title': forms.Textarea(attrs={
                'id': 'new-journal-subtitle',
            }),
            'picture': forms.FileInput(attrs={
                'id': 'image-upload',
            }),
            'date': forms.DateInput(attrs={
                'placeholder': 'Example: 2024-08-06 (year-month-day)',
            }),
            'time': forms.TimeInput(attrs={
                'placeholder': 'Example: 16:00',
            }),
        }

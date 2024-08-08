from django import forms
from .models import Article

class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'sub_title', 'body', 'field', 'picture')
    
        widgets = {
            'title': forms.Textarea(attrs={
                'id': 'new-journal-title',
                'autofocus': True,
            }),
            'sub_title': forms.Textarea(attrs={
                'id': 'new-journal-subtitle',
            }),
            'body': forms.Textarea(attrs={
                'id': 'article--body',
            }),
            'field': forms.TextInput(attrs={
                'id': 'journal-field',
            }),
            'picture': forms.FileInput(attrs={
                'id': 'image-upload',
            }),
        }

from django import forms
from .models import Journal

class AddJournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = (
            'title', 'sub_title', 'abstract', 'keywords', 'full_journal',
            'type', 'field', 'reviewed_by', 'link_to_profile', 'contributor_id_number',
            'special_note',
        )
    
        widgets = {
            'title': forms.Textarea(attrs={
                'id': 'new-journal-title',
                'autofocus': True,
            }),
            'sub_title': forms.Textarea(attrs={
                'id': 'new-journal-subtitle',
            }),
            'full_journal': forms.Textarea(attrs={
                'id': 'full--journal--body',
            }),
        }

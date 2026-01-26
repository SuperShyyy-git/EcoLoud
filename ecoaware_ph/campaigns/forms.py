from django import forms
from .models import Campaign, CampaignSuggestion

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = [
            'title',
            'description',
            'image',
            'start_date',
            'end_date',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter campaign title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your campaign'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CampaignSuggestionForm(forms.ModelForm):
    class Meta:
        model = CampaignSuggestion
        fields = ['title', 'description', 'reason']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name your campaign idea'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe what the campaign is about'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Why is this campaign important?'
            }),
        }

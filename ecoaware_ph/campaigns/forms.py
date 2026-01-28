from django import forms
from .models import Campaign, CampaignSuggestion
import json

class CampaignForm(forms.ModelForm):
    goals_input = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Plant 500+ trees and restore natural habitats\nEngage 200+ volunteers in hands-on activities\nReduce water waste by 30%'
        }),
        help_text='Enter each goal on a separate line. Simple sentences work fine!',
        label='Campaign Goals'
    )
    
    class Meta:
        model = Campaign
        fields = [
            'title',
            'description',
            'start_date',
            'end_date',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter campaign title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your campaign'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default dates for new campaigns only
        if not self.instance.pk:
            from django.utils import timezone
            from datetime import timedelta
            
            now = timezone.now()
            # Default start date: now
            # Default end date: 30 days from now
            self.initial['start_date'] = now.strftime('%Y-%m-%dT%H:%M')
            self.initial['end_date'] = (now + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M')
        
        # Convert existing goals to text format for editing
        if self.instance and self.instance.pk and self.instance.goals:
            goals_text = []
            for goal in self.instance.goals:
                goals_text.append(f"{goal.get('icon', '📌')} | {goal.get('title', '')} | {goal.get('description', '')}")
            self.initial['goals_input'] = '\n'.join(goals_text)
    
    def clean_goals_input(self):
        goals_text = self.cleaned_data.get('goals_input', '')
        if not goals_text.strip():
            return []
        
        goals = []
        goal_icons = ['🎯', '🌱', '👥', '💧', '♻️', '🌍', '📚', '🏆', '✨', '💪']
        
        for line_num, line in enumerate(goals_text.strip().split('\n'), 1):
            line = line.strip()
            if not line:
                continue
            
            # Check if it's the old pipe-separated format (for backward compatibility)
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) == 3:
                    goals.append({
                        'icon': parts[0],
                        'title': parts[1],
                        'description': parts[2]
                    })
                    continue
            
            # New simplified format: just plain text
            # Auto-generate icon and title
            icon = goal_icons[(line_num - 1) % len(goal_icons)]
            
            # Generate title from first few words (max 5 words)
            words = line.split()
            if len(words) <= 5:
                title = line
            else:
                title = ' '.join(words[:5]) + '...'
            
            # Capitalize first letter of title
            if title:
                title = title[0].upper() + title[1:]
            
            goals.append({
                'icon': icon,
                'title': title,
                'description': line
            })
        
        return goals
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Use the cleaned and parsed goals from clean_goals_input
        instance.goals = self.cleaned_data.get('goals_input', [])
        if commit:
            instance.save()
            # If we have a many-to-many field, we need to call this
            self.save_m2m()
        return instance


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

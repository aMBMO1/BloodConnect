from django import forms
from .models import Issue

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'user_email']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter issue title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the issue'}),
            'user_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email (optional)'}),
        }
        labels = {
            'title': 'Issue Title',
            'description': 'Issue Description',
            'user_email': 'Your Email',
        }

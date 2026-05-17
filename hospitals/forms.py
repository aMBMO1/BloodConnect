from django import forms
from .models import Campaign, Registration
from donations.models import UrgentRequest
from core.constants import BLOOD_TYPES


class UrgentRequestForm(forms.ModelForm):
    class Meta:
        model  = UrgentRequest
        fields = ['blood_type', 'quantity', 'deadline', 'description']
        widgets = {
            'blood_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity':   forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'deadline':   forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the urgency...'
            }),
        }
        labels = {
            'blood_type': 'Blood Type Needed',
            'quantity':   'Units (bags)',
            'deadline':   'Deadline',
            'description': 'Description',
        }

    def clean_deadline(self):
        from datetime import date
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline <= date.today():
            raise forms.ValidationError("Deadline must be a future date.")
        return deadline


class CampaignForm(forms.ModelForm):
    target_groups = forms.MultipleChoiceField(
        choices=BLOOD_TYPES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Targeted Blood Types',
        required=True,
    )

    class Meta:
        model  = Campaign
        fields = ['name', 'date', 'location', 'target_groups', 'total_capacity']
        widgets = {
            'name':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Campaign name'}),
            'date':     forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'total_capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'name':     'Campaign Name',
            'date':     'Date',
            'location': 'Location',
            'total_capacity': 'Total Capacity',
        }

    def clean_date(self):
        from datetime import date
        campaign_date = self.cleaned_data.get('date')
        if campaign_date and campaign_date <= date.today():
            raise forms.ValidationError("Campaign date must be in the future.")
        return campaign_date

    def clean_target_groups(self):
        # Returns a Python list — Django JSONField stores it automatically
        return list(self.cleaned_data['target_groups'])


class RegistrationCampaignForm(forms.ModelForm):
    class Meta:
        model  = Registration
        fields = ['time_slot']
        widgets = {
            'time_slot': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
        labels = {
            'time_slot': 'Preferred Time Slot',
        }
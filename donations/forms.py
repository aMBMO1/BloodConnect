from django import forms
from .models import Donation, AppealResponse
from core.models import Hospital


class DonationForm(forms.ModelForm):
    class Meta:
        model  = Donation
        fields = ['hospital', 'donation_date', 'notes']
        widgets = {
            'hospital':  forms.Select(attrs={'class': 'form-select'}),
            'donation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes':    forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 'placeholder': 'Notes (optional)'
            }),
        }
        labels = {
            'hospital':  'Hospital',
            'donation_date': 'Donation Date',
            'notes':    'Notes',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show validated hospitals in the dropdown
        self.fields['hospital'].queryset = Hospital.objects.filter(validated=True)

    def clean_donation_date(self):
        from datetime import date
        donation_date = self.cleaned_data.get('donation_date')
        if donation_date and donation_date > date.today():
            raise forms.ValidationError("Donation date cannot be in the future.")
        return donation_date


class AppealResponseForm(forms.ModelForm):
    class Meta:
        model  = AppealResponse
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'status': 'Your Response',
        }
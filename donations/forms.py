from django import forms
from .models import Don, ReponseAppel
from core.models import Hopital


class DonForm(forms.ModelForm):
    class Meta:
        model  = Don
        fields = ['hopital', 'date_don', 'notes']
        widgets = {
            'hopital':  forms.Select(attrs={'class': 'form-select'}),
            'date_don': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes':    forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 'placeholder': 'Notes (optional)'
            }),
        }
        labels = {
            'hopital':  'Hospital',
            'date_don': 'Donation Date',
            'notes':    'Notes',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show validated hospitals in the dropdown
        self.fields['hopital'].queryset = Hopital.objects.filter(valide=True)

    def clean_date_don(self):
        from datetime import date
        date_don = self.cleaned_data.get('date_don')
        if date_don and date_don > date.today():
            raise forms.ValidationError("Donation date cannot be in the future.")
        return date_don


class ReponseAppelForm(forms.ModelForm):
    class Meta:
        model  = ReponseAppel
        fields = ['statut']
        widgets = {
            'statut': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'statut': 'Your Response',
        }
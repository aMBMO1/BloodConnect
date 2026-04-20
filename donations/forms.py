from django import forms
from .models import Don, ReponseAppel
from core.models import Hopital


class DonForm(forms.ModelForm):
    class Meta:
        model  = Don
        fields = ['hopital', 'date_don', 'notes']
        widgets = {
            'hopital':  forms.Select(attrs={'class': 'form-select'}),
            'date_don': forms.DateInput(attrs={
                'class': 'form-control',
                'type':  'date',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows':  3,
                'placeholder': 'Notes (optional)',
            }),
        }
        labels = {
            'hopital':  'Hospital',
            'date_don': 'Donation Date',
            'notes':    'Notes',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hopital'].queryset = Hopital.objects.filter(valide=True)


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
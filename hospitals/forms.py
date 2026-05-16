from django import forms
from .models import Campagne, Inscription
from donations.models import DemandeUrgente
from core.constants import BLOOD_TYPES


class DemandeUrgenteForm(forms.ModelForm):
    class Meta:
        model  = DemandeUrgente
        fields = ['groupe_sanguin', 'quantite', 'delai', 'description']
        widgets = {
            'groupe_sanguin': forms.Select(attrs={'class': 'form-select'}),
            'quantite':       forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'delai':          forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description':    forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the urgency...'
            }),
        }
        labels = {
            'groupe_sanguin': 'Blood Type Needed',
            'quantite':       'Units (bags)',
            'delai':          'Deadline',
            'description':    'Description',
        }

    def clean_delai(self):
        from datetime import date
        delai = self.cleaned_data.get('delai')
        if delai and delai <= date.today():
            raise forms.ValidationError("Deadline must be a future date.")
        return delai


class CampagneForm(forms.ModelForm):
    groupes_cibles = forms.MultipleChoiceField(
        choices=BLOOD_TYPES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Targeted Blood Types',
        required=True,
    )

    class Meta:
        model  = Campagne
        fields = ['nom', 'date', 'lieu', 'groupes_cibles', 'capacite_totale']
        widgets = {
            'nom':            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Campaign name'}),
            'date':           forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lieu':           forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'capacite_totale': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'nom':            'Campaign Name',
            'date':           'Date',
            'lieu':           'Location',
            'capacite_totale': 'Total Capacity',
        }

    def clean_date(self):
        from datetime import date
        campagne_date = self.cleaned_data.get('date')
        if campagne_date and campagne_date <= date.today():
            raise forms.ValidationError("Campaign date must be in the future.")
        return campagne_date

    def clean_groupes_cibles(self):
        # Returns a Python list — Django JSONField stores it automatically
        return list(self.cleaned_data['groupes_cibles'])


class InscriptionCampagneForm(forms.ModelForm):
    class Meta:
        model  = Inscription
        fields = ['creneau_horaire']
        widgets = {
            'creneau_horaire': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
        labels = {
            'creneau_horaire': 'Preferred Time Slot',
        }
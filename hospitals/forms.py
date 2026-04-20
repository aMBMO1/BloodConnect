from django import forms
from .models import Campagne, Inscription
from donations.models import DemandeUrgente


class DemandeUrgenteForm(forms.ModelForm):
    class Meta:
        model  = DemandeUrgente
        fields = ['groupe_sanguin', 'quantite', 'delai', 'description']
        widgets = {
            'groupe_sanguin': forms.Select(attrs={'class': 'form-select'}),
            'quantite':       forms.NumberInput(attrs={
                'class': 'form-control',
                'min':   1,
            }),
            'delai':       forms.DateInput(attrs={
                'class': 'form-control',
                'type':  'date',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows':  4,
            }),
        }
        labels = {
            'groupe_sanguin': 'Blood Type Needed',
            'quantite':       'Number of Pouches',
            'delai':          'Deadline',
            'description':    'Description',
        }

    def clean_delai(self):
        from django.utils import timezone
        delai = self.cleaned_data.get('delai')
        if delai and delai < timezone.now().date():
            raise forms.ValidationError('Deadline cannot be in the past!')
        return delai


class CampagneForm(forms.ModelForm):
    class Meta:
        model  = Campagne
        fields = ['nom', 'date', 'lieu', 'groupes_cibles', 'capacite_totale']
        widgets = {
            'nom':  forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type':  'date',
            }),
            'lieu':           forms.TextInput(attrs={'class': 'form-control'}),
            'groupes_cibles': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Example: O+, A+, B-',
            }),
            'capacite_totale': forms.NumberInput(attrs={
                'class': 'form-control',
                'min':   1,
            }),
        }
        labels = {
            'nom':            'Campaign Name',
            'date':           'Date',
            'lieu':           'Location',
            'groupes_cibles': 'Target Blood Types',
            'capacite_totale':'Total Capacity',
        }

    def clean_date(self):
        from django.utils import timezone
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise forms.ValidationError('Date cannot be in the past!')
        return date


class InscriptionCampagneForm(forms.ModelForm):
    class Meta:
        model  = Inscription
        fields = ['creneau_horaire']
        widgets = {
            'creneau_horaire': forms.TimeInput(attrs={
                'class': 'form-control',
                'type':  'time',
            }),
        }
        labels = {
            'creneau_horaire': 'Choose Your Time Slot',
        }
from django import forms
from django.contrib.auth.models import User
from .models import Donneur, Hopital


class DonneurRegistrationForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        })
    )
    groupe_sanguin = forms.ChoiceField(
        label='Blood Type',
        choices=Donneur.BLOOD_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    sexe = forms.ChoiceField(
        label='Gender',
        choices=Donneur.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_naissance = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type':  'date',
        })
    )
    ville = forms.CharField(
        label='City',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City',
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match!')
        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        donneur = Donneur.objects.create(
            user=user,
            groupe_sanguin=self.cleaned_data['groupe_sanguin'],
            sexe=self.cleaned_data['sexe'],
            date_naissance=self.cleaned_data['date_naissance'],
            ville=self.cleaned_data['ville'],
        )
        return donneur


class HopitalRegistrationForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        })
    )
    nom = forms.CharField(
        label='Hospital Name',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hospital Name',
        })
    )
    adresse = forms.CharField(
        label='Address',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows':  3,
            'placeholder': 'Full Address',
        })
    )
    ville = forms.CharField(
        label='City',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City',
        })
    )
    agrement = forms.CharField(
        label='License Number',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'License Number',
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered!')
        return email

    def clean_agrement(self):
        agrement = self.cleaned_data.get('agrement')
        if Hopital.objects.filter(agrement=agrement).exists():
            raise forms.ValidationError('License number already registered!')
        return agrement

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match!')
        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        hopital = Hopital.objects.create(
            user=user,
            nom=self.cleaned_data['nom'],
            adresse=self.cleaned_data['adresse'],
            ville=self.cleaned_data['ville'],
            agrement=self.cleaned_data['agrement'],
        )
        return hopital





class EditDonneurForm(forms.ModelForm):

    class Meta:
        model  = Donneur
        fields = ['groupe_sanguin', 'sexe', 'date_naissance', 'ville', 'actif']
        widgets = {
            'groupe_sanguin': forms.Select(attrs={'class': 'form-select'}),
            'sexe':           forms.Select(attrs={'class': 'form-select'}),
            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type':  'date',
            }),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'groupe_sanguin': 'Blood Type',
            'sexe':           'Gender',
            'date_naissance': 'Date of Birth',
            'ville':          'City',
            'actif':          'Available to Donate',
        }
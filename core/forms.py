from django import forms
from django.contrib.auth.models import User
from .models import Donor, Hospital
from .constants import BLOOD_TYPES 


class DonorRegistrationForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    blood_type = forms.ChoiceField(
        label='Blood Type',
        choices=BLOOD_TYPES,  
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    gender = forms.ChoiceField(
        label='Gender',
        choices=Donor.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_of_birth = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    city = forms.CharField(
        label='City',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
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
        donor = Donor.objects.create(
            user=user,
            blood_type=self.cleaned_data['blood_type'],
            gender=self.cleaned_data['gender'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            city=self.cleaned_data['city'],
        )
        return donor


class HospitalRegistrationForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    name = forms.CharField(
        label='Hospital Name',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hospital Name'})
    )
    address = forms.CharField(
        label='Address',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'})
    )
    city = forms.CharField(
        label='City',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    approval = forms.CharField(
        label='License Number',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'License Number'})
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

    def clean_approval(self):
        approval = self.cleaned_data.get('approval')
        if Hospital.objects.filter(approval=approval).exists():
            raise forms.ValidationError('License number already registered!')
        return approval

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
        hospital = Hospital.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            address=self.cleaned_data['address'],
            city=self.cleaned_data['city'],
            approval=self.cleaned_data['approval'],
        )
        return hospital


class EditDonorForm(forms.ModelForm):
    """Edit donor profile — active is intentionally excluded here,
    it's toggled separately via the toggle_active view."""

    class Meta:
        model  = Donor
        fields = ['blood_type', 'gender', 'date_of_birth', 'city']  # ✅ active removed
        widgets = {
            'blood_type': forms.Select(attrs={'class': 'form-select'}),
            'gender':     forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'city':       forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'blood_type': 'Blood Type',
            'gender':     'Gender',
            'date_of_birth': 'Date of Birth',
            'city':       'City',
        }


class EditHospitalForm(forms.ModelForm):
    """Edit hospital profile — approval excluded, shouldn't change after registration."""

    class Meta:
        model  = Hospital
        fields = ['name', 'address', 'city']  # ✅ approval intentionally excluded
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city':    forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name':    'Hospital Name',
            'address': 'Address',
            'city':    'City',
        }


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
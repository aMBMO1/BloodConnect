from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import (
    DonorRegistrationForm,
    HospitalRegistrationForm,
    LoginForm,
    EditDonorForm,
    EditHospitalForm,        
)
from .models import Donor, Hospital


def home(request):
    return render(request, 'core/home.html')


def register_donor(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            donor = form.save()
            login(request, donor.user)
            messages.success(request, 'Account created! Welcome!')
            return redirect('donations:dashboard')
    else:
        form = DonorRegistrationForm()
    return render(request, 'core/register_donor.html', {'form': form})


def register_hospital(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            hospital = form.save()
            login(request, hospital.user)
            messages.warning(request, 'Account created! Waiting for admin validation.')
            return redirect('hospitals:dashboard')
    else:
        form = HospitalRegistrationForm()
    return render(request, 'core/register_hospital.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    if hasattr(user, 'donor'):
        donor = user.donor
        if request.method == 'POST':
            form = EditDonorForm(request.POST, instance=donor)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated!')
                return redirect('core:profile')
        else:
            form = EditDonorForm(instance=donor)
        return render(request, 'core/profile_donor.html', {
            'donor': donor,
            'form':    form,
        })
    elif hasattr(user, 'hospital'):
        hospital = user.hospital
        if request.method == 'POST':
            form = EditHospitalForm(request.POST, instance=hospital)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated!')
                return redirect('core:profile')
        else:
            form = EditHospitalForm(instance=hospital)
        return render(request, 'core/profile_hospital.html', {
            'hospital': hospital,
            'form':    form,
        })
    else:
        return redirect('admin:index')


@login_required
@require_POST  
def toggle_active(request):
    """Allow a donor to deactivate/reactivate their own account."""
    if not hasattr(request.user, 'donor'):
        messages.error(request, 'Not a donor account.')
        return redirect('core:home')
    donor       = request.user.donor
    donor.active = not donor.active
    donor.save()
    status = 'activated' if donor.active else 'deactivated'
    messages.success(request, f'Your account has been {status}.')
    return redirect('core:profile')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user     = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                if hasattr(user, 'donor'):
                    return redirect('donations:dashboard')
                elif hasattr(user, 'hospital'):
                    return redirect('hospitals:dashboard')
                elif user.is_superuser:
                    return redirect('admin_panel:dashboard')
                else:
                    return redirect('core:home')
            else:
                messages.error(request, 'Invalid username or password!')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


@require_POST  
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out!')
    return redirect('core:home')
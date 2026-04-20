from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import (
    DonneurRegistrationForm,
    HopitalRegistrationForm,
    LoginForm,
    EditDonneurForm,
)
from .models import Donneur, Hopital


def home(request):
    return render(request, 'core/home.html')


def register_donneur(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = DonneurRegistrationForm(request.POST)
        if form.is_valid():
            donneur = form.save()
            login(request, donneur.user)
            messages.success(request, 'Account created! Welcome!')
            return redirect('donations:dashboard')
    else:
        form = DonneurRegistrationForm()
    return render(request, 'core/register_donneur.html', {'form': form})


def register_hopital(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = HopitalRegistrationForm(request.POST)
        if form.is_valid():
            hopital = form.save()
            login(request, hopital.user)
            messages.warning(
                request,
                'Account created! Waiting for admin validation.'
            )
            return redirect('hospitals:dashboard')
    else:
        form = HopitalRegistrationForm()
    return render(request, 'core/register_hopital.html', {'form': form})




@login_required
def profile(request):
    user = request.user
    if hasattr(user, 'donneur'):
        donneur = user.donneur
        if request.method == 'POST':
            form = EditDonneurForm(request.POST, instance=donneur)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated!')
                return redirect('core:profile')
        else:
            form = EditDonneurForm(instance=donneur)
        return render(request, 'core/profile_donneur.html', {
            'donneur': donneur,
            'form':    form,
        })
    elif hasattr(user, 'hopital'):
        return render(request, 'core/profile_hopital.html', {
            'hopital': user.hopital,
        })
    else:
        return redirect('admin:index')
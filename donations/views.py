# donations/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Don, DemandeUrgente, ReponseAppel
from .forms  import DonForm, ReponseAppelForm
from .utils  import get_next_eligible_date, is_eligible, get_compatible_blood_types
from datetime import date

def get_donneur_or_redirect(request):
    if not hasattr(request.user, 'donneur'):
        messages.error(request, 'You must be a donor.')
        return None, redirect('core:home')
    return request.user.donneur, None


@login_required
def dashboard(request):
    donneur, redir = get_donneur_or_redirect(request)
    if redir:
        return redir

    dons              = Don.objects.filter(donneur=donneur).order_by('-date_don')
    next_date         = get_next_eligible_date(donneur)
    is_eligible_now   = is_eligible(donneur)
    compatible_groups = get_compatible_blood_types(donneur.groupe_sanguin)

    demandes = DemandeUrgente.objects.filter(
        groupe_sanguin__in=compatible_groups,
        statut='active'
    ).order_by('-created_at')

    inscriptions = donneur.inscriptions.select_related('campagne').filter(
    campagne__date__gte=date.today()   # ✅ only future campaigns
).order_by('campagne__date')

    context = {
        'donneur':      donneur,
        'dons':         dons,
        'next_date':    next_date,
        'is_eligible':  is_eligible_now,
        'demandes':     demandes,
        'inscriptions': inscriptions,
        'total_dons':   dons.count(),
    }
    return render(request, 'donations/dashboard.html', context)


@login_required
def mes_dons(request):
    donneur, redir = get_donneur_or_redirect(request)
    if redir:
        return redir
    dons = Don.objects.filter(donneur=donneur).order_by('-date_don')
    return render(request, 'donations/mes_dons.html', {
        'dons': dons, 'total_dons': dons.count()
    })


@login_required
def enregistrer_don(request):
    donneur, redir = get_donneur_or_redirect(request)
    if redir:
        return redir
    if not is_eligible(donneur):
        next_date = get_next_eligible_date(donneur)
        messages.error(request, f'Not eligible yet. Next date: {next_date}')
        return redirect('donations:dashboard')
    if request.method == 'POST':
        form = DonForm(request.POST)
        if form.is_valid():
            don         = form.save(commit=False)
            don.donneur = donneur
            don.valide = True  
            don.save()
            messages.success(request, 'Donation recorded! Thank you!')
            return redirect('donations:mes_dons')
    else:
        form = DonForm()
    return render(request, 'donations/enregistrer_don.html', {
        'form': form, 'donneur': donneur
    })


@login_required
def appels_urgents(request):
    donneur, redir = get_donneur_or_redirect(request)
    if redir:
        return redir
    compatible_groups = get_compatible_blood_types(donneur.groupe_sanguin)
    demandes = DemandeUrgente.objects.filter(
        groupe_sanguin__in=compatible_groups,
        statut='active'
    ).order_by('delai')
    already_responded = ReponseAppel.objects.filter(
        donneur=donneur
    ).values_list('demande_id', flat=True)
    return render(request, 'donations/appels_urgents.html', {
        'demandes':          demandes,
        'donneur':           donneur,
        'already_responded': already_responded,
        'is_eligible':       is_eligible(donneur),
    })


@login_required
def repondre_appel(request, demande_id):
    donneur, redir = get_donneur_or_redirect(request)
    if redir:
        return redir
    demande = get_object_or_404(DemandeUrgente, id=demande_id)

    compatible_groups = get_compatible_blood_types(donneur.groupe_sanguin)
    if demande.groupe_sanguin not in compatible_groups:
        messages.error(request, 'Your blood type is not compatible with this request.')
        return redirect('donations:appels_urgents')

    if not is_eligible(donneur):
        messages.error(request, 'You are not eligible yet.')
        return redirect('donations:appels_urgents')

    if ReponseAppel.objects.filter(donneur=donneur, demande=demande).exists():
        messages.warning(request, 'Already responded!')
        return redirect('donations:appels_urgents')

    if demande.statut != 'active':
        messages.error(request, 'This request is closed.')
        return redirect('donations:appels_urgents')

    if request.method == 'POST':
        form = ReponseAppelForm(request.POST)
        if form.is_valid():
            reponse         = form.save(commit=False)
            reponse.donneur = donneur
            reponse.demande = demande
            reponse.save()
            messages.success(request, 'Response recorded!')
            return redirect('donations:appels_urgents')
    else:
        form = ReponseAppelForm()
    return render(request, 'donations/repondre_appel.html', {
        'form': form, 'demande': demande, 'donneur': donneur
    })


@login_required
def mes_reponses(request):
    donneur, redir = get_donneur_or_redirect(request)
    if redir:
        return redir
    reponses = ReponseAppel.objects.filter(
        donneur=donneur
    ).select_related('demande', 'demande__hopital').order_by('-date_reponse')
    return render(request, 'donations/mes_reponses.html', {'reponses': reponses})


@login_required
def modifier_don(request, don_id):
    donneur, redir = get_donneur_or_redirect(request)
    if redir:
        return redir
    don = get_object_or_404(Don, id=don_id, donneur=donneur)
    if request.method == 'POST':
        form = DonForm(request.POST, instance=don)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation updated!')
            return redirect('donations:mes_dons')
    else:
        form = DonForm(instance=don)
    return render(request, 'donations/modifier_don.html', {
        'form': form, 'don': don
    })


@login_required
def supprimer_don(request, don_id):
    donneur, redir = get_donneur_or_redirect(request)
    if redir:
        return redir
    don = get_object_or_404(Don, id=don_id, donneur=donneur)
    if request.method == 'POST':
        don.delete()
        messages.success(request, 'Donation deleted.')
        return redirect('donations:mes_dons')
    return render(request, 'donations/supprimer_don.html', {'don': don})
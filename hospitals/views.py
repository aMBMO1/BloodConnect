from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Campagne, Inscription
from .forms  import DemandeUrgenteForm, CampagneForm, InscriptionCampagneForm
from donations.models import DemandeUrgente, ReponseAppel
from core.models import Hopital, Donneur


def get_hopital_or_redirect(request):
    if not hasattr(request.user, 'hopital'):
        messages.error(request, 'You must be a hospital.')
        return None, redirect('core:home')
    return request.user.hopital, None


@login_required
def dashboard(request):
    hopital, redir = get_hopital_or_redirect(request)
    if redir:
        return redir
    if not hopital.valide:
        messages.warning(request, 'Pending admin validation.')
    demandes         = DemandeUrgente.objects.filter(hopital=hopital).order_by('-created_at')
    campagnes        = Campagne.objects.filter(hopital=hopital).order_by('-date')
    demandes_actives = demandes.filter(statut='active').count()
    total_reponses   = ReponseAppel.objects.filter(demande__hopital=hopital).count()
    context = {
        'hopital':          hopital,
        'demandes':         demandes,
        'campagnes':        campagnes,
        'demandes_actives': demandes_actives,
        'total_reponses':   total_reponses,
    }
    return render(request, 'hospitals/dashboard.html', context)


@login_required
def creer_demande(request):
    hopital, redir = get_hopital_or_redirect(request)
    if redir:
        return redir
    if not hopital.valide:
        messages.error(request, 'Hospital must be validated first.')
        return redirect('hospitals:dashboard')
    if request.method == 'POST':
        form = DemandeUrgenteForm(request.POST)
        if form.is_valid():
            demande         = form.save(commit=False)
            demande.hopital = hopital
            demande.save()
            messages.success(request, 'Request created!')
            return redirect('hospitals:dashboard')
    else:
        form = DemandeUrgenteForm()
    return render(request, 'hospitals/creer_demande.html', {
        'form':    form,
        'hopital': hopital,
    })


@login_required
def modifier_demande(request, demande_id):
    hopital, redir = get_hopital_or_redirect(request)
    if redir:
        return redir
    demande = get_object_or_404(DemandeUrgente, id=demande_id, hopital=hopital)
    if request.method == 'POST':
        form = DemandeUrgenteForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            messages.success(request, 'Request updated!')
            return redirect('hospitals:voir_demande', demande_id=demande.id)
    else:
        form = DemandeUrgenteForm(instance=demande)
    return render(request, 'hospitals/modifier_demande.html', {
        'form':    form,
        'demande': demande,
    })


@login_required
def voir_demande(request, demande_id):
    hopital, redir = get_hopital_or_redirect(request)
    if redir:
        return redir
    demande  = get_object_or_404(DemandeUrgente, id=demande_id, hopital=hopital)
    reponses = ReponseAppel.objects.filter(
        demande=demande
    ).select_related('donneur__user').order_by('-date_reponse')
    return render(request, 'hospitals/voir_demande.html', {
        'demande':  demande,
        'reponses': reponses,
    })


@login_required
def cloturer_demande(request, demande_id):
    hopital, redir = get_hopital_or_redirect(request)
    if redir:
        return redir
    demande        = get_object_or_404(DemandeUrgente, id=demande_id, hopital=hopital)
    demande.statut = 'closed'
    demande.save()
    messages.success(request, 'Request closed.')
    return redirect('hospitals:dashboard')


@login_required
def creer_campagne(request):
    hopital, redir = get_hopital_or_redirect(request)
    if redir:
        return redir
    if not hopital.valide:
        messages.error(request, 'Hospital must be validated first.')
        return redirect('hospitals:dashboard')
    if request.method == 'POST':
        form = CampagneForm(request.POST)
        if form.is_valid():
            campagne         = form.save(commit=False)
            campagne.hopital = hopital
            campagne.save()
            messages.success(request, 'Campaign created!')
            return redirect('hospitals:dashboard')
    else:
        form = CampagneForm()
    return render(request, 'hospitals/creer_campagne.html', {
        'form':    form,
        'hopital': hopital,
    })


@login_required
def detail_campagne(request, campagne_id):
    hopital, redir = get_hopital_or_redirect(request)
    if redir:
        return redir
    campagne     = get_object_or_404(Campagne, id=campagne_id, hopital=hopital)
    inscriptions = Inscription.objects.filter(
        campagne=campagne
    ).select_related('donneur__user').order_by('creneau_horaire')
    return render(request, 'hospitals/detail_campagne.html', {
        'campagne':     campagne,
        'inscriptions': inscriptions,
    })


@login_required
def inscrire_campagne(request, campagne_id):
    if not hasattr(request.user, 'donneur'):
        messages.error(request, 'You must be a donor.')
        return redirect('core:home')
    donneur  = request.user.donneur
    campagne = get_object_or_404(Campagne, id=campagne_id)
    if campagne.est_pleine():
        messages.error(request, 'Campaign is full!')
        return redirect('hospitals:liste_campagnes')
    if Inscription.objects.filter(campagne=campagne, donneur=donneur).exists():
        messages.warning(request, 'Already registered!')
        return redirect('hospitals:liste_campagnes')
    if request.method == 'POST':
        form = InscriptionCampagneForm(request.POST)
        if form.is_valid():
            inscription          = form.save(commit=False)
            inscription.campagne = campagne
            inscription.donneur  = donneur
            inscription.save()
            messages.success(request, f'Registered for {campagne.nom}!')
            return redirect('donations:dashboard')
    else:
        form = InscriptionCampagneForm()
    return render(request, 'hospitals/inscrire_campagne.html', {
        'form':     form,
        'campagne': campagne,
        'donneur':  donneur,
    })


@login_required
def liste_campagnes(request):
    campagnes_raw = Campagne.objects.all().order_by('date')
    campagnes     = []
    for campagne in campagnes_raw:
        filled  = campagne.inscriptions.count()
        total   = campagne.capacite_totale
        percent = int((filled / total) * 100) if total > 0 else 0
        campagnes.append({
            'obj':       campagne,
            'filled':    filled,
            'total':     total,
            'percent':   percent,
            'restantes': total - filled,
            'est_pleine': filled >= total,
        })
    return render(request, 'hospitals/liste_campagnes.html', {
        'campagnes': campagnes,
    })
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse
import csv

from core.models      import Donneur, Hopital
from donations.models import Don, DemandeUrgente, ReponseAppel
from hospitals.models import Campagne, Inscription

@staff_member_required
def dashboard(request):
    total_donneurs       = Donneur.objects.count()
    total_dons           = Don.objects.count()
    total_hopitaux       = Hopital.objects.count()
    hopitaux_non_valides = Hopital.objects.filter(valide=False).count()
    total_demandes       = DemandeUrgente.objects.filter(statut='active').count()
    total_campagnes      = Campagne.objects.count()

    dons_par_groupe = []
    for blood_type in ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']:
        count = Don.objects.filter(
            donneur__groupe_sanguin=blood_type
        ).count()
        if total_dons > 0:
            percent = int((count / total_dons) * 100)
        else:
            percent = 0
        dons_par_groupe.append({
            'blood_type': blood_type,
            'count':      count,
            'percent':    percent,
        })

    demandes_par_groupe = []
    for blood_type in ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']:
        count = DemandeUrgente.objects.filter(
            groupe_sanguin=blood_type,
            statut='active'
        ).count()
        if total_demandes > 0:
            percent = int((count / total_demandes) * 100)
        else:
            percent = 0
        demandes_par_groupe.append({
            'blood_type': blood_type,
            'count':      count,
            'percent':    percent,
        })

    context = {
        'total_donneurs':       total_donneurs,
        'total_dons':           total_dons,
        'total_hopitaux':       total_hopitaux,
        'hopitaux_non_valides': hopitaux_non_valides,
        'total_demandes':       total_demandes,
        'total_campagnes':      total_campagnes,
        'dons_par_groupe':      dons_par_groupe,
        'demandes_par_groupe':  demandes_par_groupe,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@staff_member_required
def hopitaux_list(request):
    hopitaux = Hopital.objects.all().select_related('user').order_by('valide', 'nom')
    context  = {'hopitaux': hopitaux}
    return render(request, 'admin_panel/hopitaux_list.html', context)


@staff_member_required
def valider_hopital(request, hopital_id):
    hopital        = get_object_or_404(Hopital, id=hopital_id)
    hopital.valide = True
    hopital.save()
    messages.success(request, f'Hospital "{hopital.nom}" validated!')
    return redirect('admin_panel:hopitaux_list')


@staff_member_required
def rejeter_hopital(request, hopital_id):
    hopital        = get_object_or_404(Hopital, id=hopital_id)
    hopital.valide = False
    hopital.save()
    messages.warning(request, f'Hospital "{hopital.nom}" deactivated.')
    return redirect('admin_panel:hopitaux_list')


@staff_member_required
def donneurs_list(request):
    donneurs = Donneur.objects.all().select_related('user').order_by('user__username')
    context  = {'donneurs': donneurs}
    return render(request, 'admin_panel/donneurs_list.html', context)


@staff_member_required
def export_donneurs_csv(request):
    donneurs  = Donneur.objects.all().select_related('user')
    response  = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="donneurs.csv"'
    writer    = csv.writer(response)

    writer.writerow([
        'Username',
        'Email',
        'Blood Type',
        'Gender',
        'Date of Birth',
        'City',
        'Active',
        'Total Donations',
    ])

    for donneur in donneurs:
        writer.writerow([
            donneur.user.username,
            donneur.user.email,
            donneur.groupe_sanguin,
            donneur.get_sexe_display(),
            donneur.date_naissance,
            donneur.ville,
            donneur.actif,
            Don.objects.filter(donneur=donneur).count(),
        ])

    return response


@staff_member_required
def statistiques(request):
    total_dons      = Don.objects.count()
    total_demandes  = DemandeUrgente.objects.filter(statut='active').count()

    dons_par_groupe = []
    for blood_type in ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']:
        count = Don.objects.filter(
            donneur__groupe_sanguin=blood_type
        ).count()
        if total_dons > 0:
            percent = int((count / total_dons) * 100)
        else:
            percent = 0
        dons_par_groupe.append({
            'blood_type': blood_type,
            'count':      count,
            'percent':    percent,
        })

    donneurs_par_ville = {}
    for donneur in Donneur.objects.all():
        ville = donneur.ville
        donneurs_par_ville[ville] = donneurs_par_ville.get(ville, 0) + 1

    demandes_par_ville = {}
    for demande in DemandeUrgente.objects.filter(
        statut='active'
    ).select_related('hopital'):
        ville = demande.hopital.ville
        demandes_par_ville[ville] = demandes_par_ville.get(ville, 0) + 1

    demandes_par_groupe = []
    for blood_type in ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']:
        count = DemandeUrgente.objects.filter(
            groupe_sanguin=blood_type,
            statut='active'
        ).count()
        if total_demandes > 0:
            percent = int((count / total_demandes) * 100)
        else:
            percent = 0
        demandes_par_groupe.append({
            'blood_type': blood_type,
            'count':      count,
            'percent':    percent,
        })

    context = {
        'dons_par_groupe':    dons_par_groupe,
        'donneurs_par_ville': donneurs_par_ville,
        'demandes_par_ville': demandes_par_ville,
        'demandes_par_groupe':demandes_par_groupe,
        'total_dons':         total_dons,
        'total_demandes':     total_demandes,
    }
    return render(request, 'admin_panel/statistiques.html', context)
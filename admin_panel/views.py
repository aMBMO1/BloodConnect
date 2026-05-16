# admin_panel/views.py
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count

from core.models import Donneur, Hopital
from donations.models import Don, DemandeUrgente
from hospitals.models import Campagne


@staff_member_required
def dashboard(request):
    total_donneurs       = Donneur.objects.count()
    total_hopitaux       = Hopital.objects.count()
    total_dons           = Don.objects.count()
    hopitaux_non_valides = Hopital.objects.filter(valide=False).count()
    total_demandes       = DemandeUrgente.objects.filter(statut='active').count()
    total_campagnes      = Campagne.objects.count()

    dons_qs = (
        Don.objects
        .values('donneur__groupe_sanguin')
        .annotate(count=Count('id'))
        .order_by('donneur__groupe_sanguin')
    )
    dons_par_groupe = [
        {
            'blood_type': item['donneur__groupe_sanguin'],
            'count':      item['count'],
            'percent':    round(item['count'] / total_dons * 100) if total_dons else 0,
        }
        for item in dons_qs
    ]

    demandes_qs = (
        DemandeUrgente.objects
        .filter(statut='active')
        .values('groupe_sanguin')
        .annotate(count=Count('id'))
        .order_by('groupe_sanguin')
    )
    demandes_par_groupe = [
        {
            'blood_type': item['groupe_sanguin'],
            'count':      item['count'],
            'percent':    round(item['count'] / total_demandes * 100) if total_demandes else 0,
        }
        for item in demandes_qs
    ]

    context = {
        'total_donneurs':       total_donneurs,
        'total_hopitaux':       total_hopitaux,
        'total_dons':           total_dons,
        'hopitaux_non_valides': hopitaux_non_valides,
        'total_demandes':       total_demandes,
        'total_campagnes':      total_campagnes,
        'dons_par_groupe':      dons_par_groupe,
        'demandes_par_groupe':  demandes_par_groupe,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@staff_member_required
def hopitaux_list(request):
    hopitaux = Hopital.objects.select_related('user').order_by('valide', 'nom')
    return render(request, 'admin_panel/hopitaux_list.html', {'hopitaux': hopitaux})


@staff_member_required
def valider_hopital(request, hopital_id):
    hopital        = get_object_or_404(Hopital, id=hopital_id)
    hopital.valide = True
    hopital.save()
    messages.success(request, f'"{hopital.nom}" has been validated.')
    return redirect('admin_panel:hopitaux_list')


@staff_member_required
def rejeter_hopital(request, hopital_id):
    hopital = get_object_or_404(Hopital, id=hopital_id)
    nom     = hopital.nom
    hopital.user.delete()  # cascades to Hopital automatically
    messages.warning(request, f'"{nom}" has been rejected and removed.')
    return redirect('admin_panel:hopitaux_list')


@staff_member_required
def donneurs_list(request):
    donneurs = (
        Donneur.objects
        .select_related('user')
        .annotate(total_dons=Count('dons'))
        .order_by('user__username')
    )
    return render(request, 'admin_panel/donneurs_list.html', {'donneurs': donneurs})


@staff_member_required
def valider_don(request, don_id):
    don        = get_object_or_404(Don, id=don_id)
    don.valide = True
    don.save()
    messages.success(request, f'Donation by {don.donneur.user.username} validated.')
    return redirect('admin_panel:donneurs_list')


@staff_member_required
def export_donneurs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="donneurs.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Username', 'Email', 'First Name', 'Last Name',
        'Groupe Sanguin', 'Sexe', 'Date Naissance', 'Ville', 'Actif', 'Total Dons',
    ])

    donneurs = (
        Donneur.objects
        .select_related('user')
        .annotate(total_dons=Count('dons'))
        .order_by('user__username')
    )
    for d in donneurs:
        writer.writerow([
            d.user.username,
            d.user.email,
            d.user.first_name,
            d.user.last_name,
            d.groupe_sanguin,
            d.get_sexe_display(),
            d.date_naissance,
            d.ville,
            'Yes' if d.actif else 'No',
            d.total_dons,
        ])

    return response

@staff_member_required
def campagnes_list(request):
    from hospitals.models import Campagne
    campagnes = Campagne.objects.select_related('hopital').annotate(
        total_inscriptions=Count('inscriptions')
    ).order_by('-date')
    return render(request, 'admin_panel/campagnes_list.html', {'campagnes': campagnes})
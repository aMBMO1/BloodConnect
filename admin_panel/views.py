import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count

from core.models import Donor, Hospital
from donations.models import Donation, UrgentRequest
from hospitals.models import Campaign


@staff_member_required
def dashboard(request):
    total_donors       = Donor.objects.count()
    total_hospitals    = Hospital.objects.count()
    total_donations    = Donation.objects.count()
    hospitals_unvalidated = Hospital.objects.filter(validated=False).count()
    total_requests     = UrgentRequest.objects.filter(status='active').count()
    total_campaigns    = Campaign.objects.count()

    donations_qs = (
        Donation.objects
        .values('donor__blood_type')
        .annotate(count=Count('id'))
        .order_by('donor__blood_type')
    )
    donations_by_blood_type = [
        {
            'blood_type': item['donor__blood_type'],
            'count':      item['count'],
            'percent':    round(item['count'] / total_donations * 100) if total_donations else 0,
        }
        for item in donations_qs
    ]

    requests_qs = (
        UrgentRequest.objects
        .filter(status='active')
        .values('blood_type')
        .annotate(count=Count('id'))
        .order_by('blood_type')
    )
    requests_by_blood_type = [
        {
            'blood_type': item['blood_type'],
            'count':      item['count'],
            'percent':    round(item['count'] / total_requests * 100) if total_requests else 0,
        }
        for item in requests_qs
    ]

    context = {
        'total_donors':           total_donors,
        'total_hospitals':        total_hospitals,
        'total_donations':        total_donations,
        'hospitals_unvalidated':  hospitals_unvalidated,
        'total_requests':         total_requests,
        'total_campaigns':        total_campaigns,
        'donations_by_blood_type': donations_by_blood_type,
        'requests_by_blood_type': requests_by_blood_type,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@staff_member_required
def hospitals_list(request):
    hospitals = Hospital.objects.select_related('user').order_by('validated', 'name')
    return render(request, 'admin_panel/hospitals_list.html', {'hospitals': hospitals})


@staff_member_required
def validate_hospital(request, hospital_id):
    hospital        = get_object_or_404(Hospital, id=hospital_id)
    hospital.validated = True
    hospital.save()
    messages.success(request, f'"{hospital.name}" has been validated.')
    return redirect('admin_panel:hospitals_list')


@staff_member_required
def reject_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    name     = hospital.name
    hospital.user.delete()  # cascades to Hospital automatically
    messages.warning(request, f'"{name}" has been rejected and removed.')
    return redirect('admin_panel:hospitals_list')


@staff_member_required
def donors_list(request):
    donors = (
        Donor.objects
        .select_related('user')
        .annotate(total_donations=Count('donations'))
        .order_by('user__username')
    )
    return render(request, 'admin_panel/donors_list.html', {'donors': donors})


@staff_member_required
def validate_donation(request, donation_id):
    donation        = get_object_or_404(Donation, id=donation_id)
    donation.validated = True
    donation.save()
    messages.success(request, f'Donation by {donation.donor.user.username} validated.')
    return redirect('admin_panel:donors_list')


@staff_member_required
def export_donors_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="donors.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Username', 'Email', 'First Name', 'Last Name',
        'Blood Type', 'Gender', 'Date of Birth', 'City', 'Active', 'Total Donations',
    ])

    donors = (
        Donor.objects
        .select_related('user')
        .annotate(total_donations=Count('donations'))
        .order_by('user__username')
    )
    for d in donors:
        writer.writerow([
            d.user.username,
            d.user.email,
            d.user.first_name,
            d.user.last_name,
            d.blood_type,
            d.get_gender_display(),
            d.date_of_birth,
            d.city,
            'Yes' if d.active else 'No',
            d.total_donations,
        ])

    return response

@staff_member_required
def campaigns_list(request):
    from hospitals.models import Campaign
    campaigns = Campaign.objects.select_related('hospital').annotate(
        total_registrations=Count('registrations')
    ).order_by('-date')
    return render(request, 'admin_panel/campaigns_list.html', {'campaigns': campaigns})
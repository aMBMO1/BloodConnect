from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Donation, UrgentRequest, AppealResponse
from .forms  import DonationForm, AppealResponseForm
from .utils  import get_next_eligible_date, is_eligible, get_compatible_blood_types
from datetime import date

def get_donor_or_redirect(request):
    if not hasattr(request.user, 'donor'):
        messages.error(request, 'You must be a donor.')
        return None, redirect('core:home')
    return request.user.donor, None


@login_required
def dashboard(request):
    donor, redir = get_donor_or_redirect(request)
    if redir:
        return redir

    donations         = Donation.objects.filter(donor=donor).order_by('-donation_date')
    next_date         = get_next_eligible_date(donor)
    is_eligible_now   = is_eligible(donor)
    compatible_groups = get_compatible_blood_types(donor.blood_type)

    requests = UrgentRequest.objects.filter(
        blood_type__in=compatible_groups,
        status='active'
    ).order_by('-created_at')

    registrations = donor.registrations.select_related('campaign').filter(
    campaign__date__gte=date.today()  
).order_by('campaign__date')

    context = {
        'donor':         donor,
        'donations':     donations,
        'next_date':     next_date,
        'is_eligible':   is_eligible_now,
        'requests':      requests,
        'registrations': registrations,
        'total_donations': donations.count(),
    }
    return render(request, 'donations/dashboard.html', context)


@login_required
def my_donations(request):
    donor, redir = get_donor_or_redirect(request)
    if redir:
        return redir
    donations = Donation.objects.filter(donor=donor).order_by('-donation_date')
    return render(request, 'donations/my_donations.html', {
        'donations': donations, 'total_donations': donations.count()
    })


@login_required
def register_donation(request):
    donor, redir = get_donor_or_redirect(request)
    if redir:
        return redir
    if not is_eligible(donor):
        next_date = get_next_eligible_date(donor)
        messages.error(request, f'Not eligible yet. Next date: {next_date}')
        return redirect('donations:dashboard')
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation       = form.save(commit=False)
            donation.donor = donor
            donation.validated = True  
            donation.save()
            messages.success(request, 'Donation recorded! Thank you!')
            return redirect('donations:my_donations')
    else:
        form = DonationForm()
    return render(request, 'donations/register_donation.html', {
        'form': form, 'donor': donor
    })


@login_required
def urgent_appeals(request):
    donor, redir = get_donor_or_redirect(request)
    if redir:
        return redir
    compatible_groups = get_compatible_blood_types(donor.blood_type)
    requests = UrgentRequest.objects.filter(
        blood_type__in=compatible_groups,
        status='active'
    ).order_by('deadline')
    already_responded = AppealResponse.objects.filter(
        donor=donor
    ).values_list('request_id', flat=True)

    has_active_response = AppealResponse.objects.filter(
        donor=donor,
        status__in=['interested', 'confirmed'],
        request__status='active'
    ).exists()

    return render(request, 'donations/urgent_appeals.html', {
        'requests':           requests,
        'donor':              donor,
        'already_responded':  already_responded,
        'is_eligible':        is_eligible(donor),
        'has_active_response': has_active_response
    })


@login_required
def respond_to_appeal(request, request_id):
    donor, redir = get_donor_or_redirect(request)
    if redir:
        return redir
    urgent_request = get_object_or_404(UrgentRequest, id=request_id)

    compatible_groups = get_compatible_blood_types(donor.blood_type)
    if urgent_request.blood_type not in compatible_groups:
        messages.error(request, 'Your blood type is not compatible with this request.')
        return redirect('donations:urgent_appeals')

    if not is_eligible(donor):
        messages.error(request, 'You are not eligible yet.')
        return redirect('donations:urgent_appeals')

    if AppealResponse.objects.filter(donor=donor, request=urgent_request).exists():
        messages.warning(request, 'Already responded!')
        return redirect('donations:urgent_appeals')

    if urgent_request.status != 'active':
        messages.error(request, 'This request is closed.')
        return redirect('donations:urgent_appeals')
    active_response = AppealResponse.objects.filter(
        donor=donor,
        status__in=['interested', 'confirmed'],
        request__status='active'
    ).exists()
    if active_response:
        messages.error(request, 'You already responded to an active request. Please wait until it is resolved before responding to another one.')
        return redirect('donations:urgent_appeals')

    if request.method == 'POST':
        form = AppealResponseForm(request.POST)
        if form.is_valid():
            response       = form.save(commit=False)
            response.donor = donor
            response.request = urgent_request
            response.save()
            messages.success(request, 'Response recorded!')
            return redirect('donations:urgent_appeals')
    else:
        form = AppealResponseForm()
    return render(request, 'donations/respond_to_appeal.html', {
        'form': form, 'request': urgent_request, 'donor': donor
    })


@login_required
def my_responses(request):
    donor, redir = get_donor_or_redirect(request)
    if redir:
        return redir
    responses = AppealResponse.objects.filter(
        donor=donor
    ).select_related('request', 'request__hospital').order_by('-response_date')
    return render(request, 'donations/my_responses.html', {'responses': responses})


@login_required
def modify_donation(request, donation_id):
    donor, redir = get_donor_or_redirect(request)
    if redir:
        return redir
    donation = get_object_or_404(Donation, id=donation_id, donor=donor)
    if request.method == 'POST':
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation updated!')
            return redirect('donations:my_donations')
    else:
        form = DonationForm(instance=donation)
    return render(request, 'donations/modify_donation.html', {
        'form': form, 'donation': donation
    })


@login_required
def delete_donation(request, donation_id):
    donor, redir = get_donor_or_redirect(request)
    if redir:
        return redir
    donation = get_object_or_404(Donation, id=donation_id, donor=donor)
    if request.method == 'POST':
        donation.delete()
        messages.success(request, 'Donation deleted.')
        return redirect('donations:my_donations')
    return render(request, 'donations/delete_donation.html', {'donation': donation})
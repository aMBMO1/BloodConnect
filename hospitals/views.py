# hospitals/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Count

from .models import Campaign, Registration
from .forms  import UrgentRequestForm, CampaignForm, RegistrationCampaignForm
from donations.models import UrgentRequest, AppealResponse
from core.models import Hospital, Donor
from donations.utils import get_compatible_blood_types


def get_hospital_or_redirect(request):
    if not hasattr(request.user, 'hospital'):
        messages.error(request, 'You must be a hospital.')
        return None, redirect('core:home')
    return request.user.hospital, None


@login_required
def dashboard(request):
    hospital, redir = get_hospital_or_redirect(request)
    if redir:
        return redir
    if not hospital.validated:
        messages.warning(request, 'Pending admin validation.')
    requests         = UrgentRequest.objects.filter(hospital=hospital).order_by('-created_at')
    campaigns        = Campaign.objects.filter(hospital=hospital).order_by('-date')
    active_requests = requests.filter(status='active').count()
    total_responses  = AppealResponse.objects.filter(request__hospital=hospital).count()
    return render(request, 'hospitals/dashboard.html', {
        'hospital':        hospital,
        'requests':        requests,
        'campaigns':       campaigns,
        'active_requests': active_requests,
        'total_responses': total_responses,
    })


@login_required
def create_request(request):
    hospital, redir = get_hospital_or_redirect(request)
    if redir:
        return redir
    if not hospital.validated:
        messages.error(request, 'Hospital must be validated first.')
        return redirect('hospitals:dashboard')
    if request.method == 'POST':
        form = UrgentRequestForm(request.POST)
        if form.is_valid():
            urgent_request    = form.save(commit=False)
            urgent_request.hospital = hospital
            urgent_request.save()
            messages.success(request, 'Request created!')
            return redirect('hospitals:dashboard')
    else:
        form = UrgentRequestForm()
    return render(request, 'hospitals/create_request.html', {
        'form': form, 'hospital': hospital
    })


@login_required
def modify_request(request, request_id):
    hospital, redir = get_hospital_or_redirect(request)
    if redir:
        return redir
    urgent_request = get_object_or_404(UrgentRequest, id=request_id, hospital=hospital)
    if request.method == 'POST':
        form = UrgentRequestForm(request.POST, instance=urgent_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Request updated!')
            return redirect('hospitals:view_request', request_id=urgent_request.id)
    else:
        form = UrgentRequestForm(instance=urgent_request)
    return render(request, 'hospitals/modify_request.html', {
        'form': form, 'request': urgent_request
    })


@login_required
def view_request(request, request_id):
    hospital, redir = get_hospital_or_redirect(request)
    if redir:
        return redir
    urgent_request = get_object_or_404(UrgentRequest, id=request_id, hospital=hospital)
    responses = AppealResponse.objects.filter(
        request=urgent_request
    ).select_related('donor__user').order_by('-response_date')
    return render(request, 'hospitals/view_request.html', {
        'request': urgent_request, 'responses': responses
    })


@login_required
def close_request(request, request_id):
    hospital, redir = get_hospital_or_redirect(request)
    if redir:
        return redir
    urgent_request     = get_object_or_404(UrgentRequest, id=request_id, hospital=hospital)
    urgent_request.status = 'closed'
    urgent_request.save()
    messages.success(request, 'Request closed.')
    return redirect('hospitals:dashboard')


@login_required
def create_campaign(request):
    hospital, redir = get_hospital_or_redirect(request)
    if redir:
        return redir
    if not hospital.validated:
        messages.error(request, 'Hospital must be validated first.')
        return redirect('hospitals:dashboard')
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign        = form.save(commit=False)
            campaign.hospital = hospital
            campaign.save()
            messages.success(request, 'Campaign created!')
            return redirect('hospitals:dashboard')
    else:
        form = CampaignForm()
    return render(request, 'hospitals/create_campaign.html', {
        'form': form, 'hospital': hospital
    })


@login_required
def campaign_detail(request, campaign_id):
    hospital, redir = get_hospital_or_redirect(request)
    if redir:
        return redir
    campaign     = get_object_or_404(Campaign, id=campaign_id, hospital=hospital)
    registrations = Registration.objects.filter(
        campaign=campaign
    ).select_related('donor__user').order_by('time_slot')
    return render(request, 'hospitals/campaign_detail.html', {
        'campaign': campaign, 'registrations': registrations
    })


@login_required
def register_campaign(request, campaign_id):
    if not hasattr(request.user, 'donor'):
        messages.error(request, 'You must be a donor.')
        return redirect('core:home')
    donor    = request.user.donor
    campaign = get_object_or_404(Campaign, id=campaign_id)

    # ✅ check blood type on BOTH GET and POST
    if donor.blood_type not in campaign.target_groups:
        messages.error(request, 'Your blood type is not targeted by this campaign.')
        return redirect('hospitals:campaign_list')

    if Registration.objects.filter(campaign=campaign, donor=donor).exists():
        messages.warning(request, 'Already registered!')
        return redirect('hospitals:campaign_list')

    if request.method == 'POST':
        form = RegistrationCampaignForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                campaign_locked = Campaign.objects.select_for_update().get(id=campaign_id)
                if campaign_locked.is_full():
                    messages.error(request, 'Campaign is full!')
                    return redirect('hospitals:campaign_list')
                registration       = form.save(commit=False)
                registration.campaign = campaign_locked
                registration.donor   = donor
                registration.save()
            messages.success(request, f'Registered for {campaign.name}!')
            return redirect('donations:dashboard')
    else:
        if campaign.is_full():
            messages.error(request, 'Campaign is full!')
            return redirect('hospitals:campaign_list')
        form = RegistrationCampaignForm()

    return render(request, 'hospitals/register_campaign.html', {
        'form': form, 'campaign': campaign, 'donor': donor
    })

@login_required
def campaign_list(request):
    campaigns_raw = Campaign.objects.annotate(
        filled=Count('registrations')
    ).order_by('date')

    donor = getattr(request.user, 'donor', None)

    campaigns = []
    for campaign in campaigns_raw:
        total   = campaign.total_capacity
        filled  = campaign.filled
        percent = int((filled / total) * 100) if total > 0 else 0

        # ✅ FIX: campaign is compatible if it's asking for THIS donor's blood type
        # Not whether the donor can donate to others
        compatible = (
            donor.blood_type in campaign.target_groups
            if donor else True
        )

        campaigns.append({
            'obj':        campaign,
            'filled':     filled,
            'total':      total,
            'percent':    percent,
            'remaining':  total - filled,
            'is_full': filled >= total,
            'compatible': compatible,
        })

    return render(request, 'hospitals/campaign_list.html', {'campaigns': campaigns})
@login_required
def modify_campaign(request, campaign_id):
    hospital, redir = get_hospital_or_redirect(request)
    if redir:
        return redir
    campaign = get_object_or_404(Campaign, id=campaign_id, hospital=hospital)
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaign updated!')
            return redirect('hospitals:campaign_detail', campaign_id=campaign.id)
    else:
        # ✅ pre-check the existing blood types in the checkboxes
        form = CampaignForm(
            instance=campaign,
            initial={'target_groups': campaign.target_groups}
        )
    return render(request, 'hospitals/modify_campaign.html', {
        'form': form, 'campaign': campaign
    })


@login_required
def delete_campaign(request, campaign_id):
    hospital, redir = get_hospital_or_redirect(request)
    if redir:
        return redir
    campaign = get_object_or_404(Campaign, id=campaign_id, hospital=hospital)
    if request.method == 'POST':
        campaign.delete()
        messages.success(request, f'Campaign "{campaign.name}" deleted.')
        return redirect('hospitals:dashboard')
    return render(request, 'hospitals/delete_campaign.html', {'campaign': campaign})
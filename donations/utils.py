from datetime import timedelta
from django.utils import timezone

COMPATIBILITY = {
    'O-':  ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],
    'O+':  ['O+', 'A+', 'B+', 'AB+'],
    'A-':  ['A-', 'A+', 'AB-', 'AB+'],
    'A+':  ['A+', 'AB+'],
    'B-':  ['B-', 'B+', 'AB-', 'AB+'],
    'B+':  ['B+', 'AB+'],
    'AB-': ['AB-', 'AB+'],
    'AB+': ['AB+'],
}


def get_compatible_blood_types(blood_type):
    return COMPATIBILITY.get(blood_type, [])


def get_next_eligible_date(donneur):
    from donations.models import Don
    last_don = Don.objects.filter(
        donneur=donneur
    ).order_by('-date_don').first()
    if not last_don:
        return timezone.now().date()
    days = 56 if donneur.sexe == 'M' else 84
    return last_don.date_don + timedelta(days=days)


def is_eligible(donneur):
    return timezone.now().date() >= get_next_eligible_date(donneur)
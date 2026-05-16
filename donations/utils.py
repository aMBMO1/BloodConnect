# donations/utils.py
from datetime import date, timedelta
from .models import Don


# Number of days a donor must wait before donating again
ELIGIBILITY_DAYS = {
    'M': 56,   # Men: 56 days
    'F': 84,   # Women: 84 days
}

# Blood type compatibility chart
# Key = donor's blood type, Value = list of blood types they can donate to
COMPATIBILITY = {
    'O-':  ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],  # universal donor
    'O+':  ['O+', 'A+', 'B+', 'AB+'],
    'A-':  ['A-', 'A+', 'AB-', 'AB+'],
    'A+':  ['A+', 'AB+'],
    'B-':  ['B-', 'B+', 'AB-', 'AB+'],
    'B+':  ['B+', 'AB+'],
    'AB-': ['AB-', 'AB+'],
    'AB+': ['AB+'],
}


def get_last_don(donneur):
    return Don.objects.filter(
        donneur=donneur
    ).order_by('-date_don').first()  


def get_next_eligible_date(donneur):
    """
    Return the date the donor is next eligible to donate.
    Returns today's date if they have never donated (i.e. eligible now).
    """
    last_don = get_last_don(donneur)
    if last_don is None:
        return date.today()
    wait_days = ELIGIBILITY_DAYS.get(donneur.sexe, 56)
    return last_don.date_don + timedelta(days=wait_days)


def is_eligible(donneur):
    """
    Return True if the donor is allowed to donate today:
    - Their account must be active
    - The waiting period since their last donation must have passed
    """
    if not donneur.actif:
        return False
    return date.today() >= get_next_eligible_date(donneur)


def get_compatible_blood_types(blood_type):
    """
    Given a donor's blood type, return the list of blood types
    they are compatible with (i.e. the demandes they can respond to).
    """
    return COMPATIBILITY.get(blood_type, [])
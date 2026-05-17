# donations/utils.py
from datetime import date, timedelta
from .models import Donation


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


def get_last_donation(donor):
    return Donation.objects.filter(
        donor=donor
    ).order_by('-donation_date').first()  


def get_next_eligible_date(donor):
    """
    Return the date the donor is next eligible to donate.
    Returns today's date if they have never donated (i.e. eligible now).
    """
    last_donation = get_last_donation(donor)
    if last_donation is None:
        return date.today()
    wait_days = ELIGIBILITY_DAYS.get(donor.gender, 56)
    return last_donation.donation_date + timedelta(days=wait_days)


def is_eligible(donor):
    """
    Return True if the donor is allowed to donate today:
    - Their account must be active
    - The waiting period since their last donation must have passed
    """
    if not donor.active:
        return False
    return date.today() >= get_next_eligible_date(donor)


def get_compatible_blood_types(blood_type):
    """
    Given a donor's blood type, return the list of blood types
    they are compatible with (i.e. the requests they can respond to).
    """
    return COMPATIBILITY.get(blood_type, [])
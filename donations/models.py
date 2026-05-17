# donations/models.py
from django.db import models
from core.models import Donor, Hospital
from core.constants import BLOOD_TYPES


class Donation(models.Model):
    donor      = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donations')
    hospital   = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='received_donations')
    donation_date = models.DateField()
    notes      = models.TextField(blank=True)
    validated  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation by {self.donor.user.username} - {self.donation_date}"

    class Meta:
        verbose_name        = "Donation"
        verbose_name_plural = "Donations"
        ordering            = ['-donation_date']


class UrgentRequest(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]

    hospital   = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='requests')
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    quantity   = models.PositiveIntegerField()
    deadline   = models.DateField()
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blood_type} - {self.hospital.name}"

    class Meta:
        verbose_name        = "Urgent Request"
        verbose_name_plural = "Urgent Requests"
        ordering            = ['-created_at']


class AppealResponse(models.Model):
    STATUS_CHOICES = [
        ('interested', 'Interested'),
        ('confirmed',  'Confirmed'),
        ('declined',   'Declined'),
    ]

    donor      = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='responses')
    request    = models.ForeignKey(UrgentRequest, on_delete=models.CASCADE, related_name='responses')
    response_date = models.DateTimeField(auto_now_add=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='interested')

    def __str__(self):
        return f"{self.donor.user.username} - {self.request}"

    class Meta:
        verbose_name        = "Appeal Response"
        verbose_name_plural = "Appeal Responses"
        ordering            = ['-response_date']
        unique_together     = ('donor', 'request')
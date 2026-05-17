# hospitals/models.py
from django.db import models
from core.models import Hospital, Donor
from core.constants import BLOOD_TYPES, BLOOD_TYPE_VALUES


class Campaign(models.Model):
    hospital        = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='campaigns')
    name            = models.CharField(max_length=200)
    date            = models.DateField()
    location        = models.CharField(max_length=200)
    target_groups   = models.JSONField(default=list)
    total_capacity  = models.PositiveIntegerField()
    created_at      = models.DateTimeField(auto_now_add=True)

    def remaining_spots(self):
        return self.total_capacity - self.registrations.count()

    def is_full(self):
        return self.registrations.count() >= self.total_capacity

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = "Campaign"
        verbose_name_plural = "Campaigns"
        ordering            = ['-date']


class Registration(models.Model):
    campaign          = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='registrations')
    donor             = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='registrations')
    time_slot         = models.TimeField()
    registration_date = models.DateTimeField(auto_now_add=True)
    present           = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.donor.user.username} - {self.campaign.name}"

    class Meta:
        verbose_name        = "Registration"
        verbose_name_plural = "Registrations"
        unique_together     = ('campaign', 'donor')
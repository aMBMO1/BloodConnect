# core/models.py
from django.db import models
from django.contrib.auth.models import User
from .constants import BLOOD_TYPES


class Donor(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor')
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    gender     = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    city       = models.CharField(max_length=100)
    active     = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} ({self.blood_type})"

    class Meta:
        verbose_name        = "Donor"
        verbose_name_plural = "Donors"


class Hospital(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hospital')
    name       = models.CharField(max_length=200)
    address    = models.TextField()
    city       = models.CharField(max_length=100)
    approval   = models.CharField(max_length=100, unique=True)
    validated  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = "Hospital"
        verbose_name_plural = "Hospitals"
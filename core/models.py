from django.db import models
from django.contrib.auth.models import User


class Donneur(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    BLOOD_TYPES = [
        ('O+',  'O+'),
        ('O-',  'O-'),
        ('A+',  'A+'),
        ('A-',  'A-'),
        ('B+',  'B+'),
        ('B-',  'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]

    user  = models.OneToOneField(
                        User,
                        on_delete=models.CASCADE,
                        related_name='donneur'
                     )
    groupe_sanguin = models.CharField(max_length=3,  choices=BLOOD_TYPES)
    sexe           = models.CharField(max_length=1,  choices=GENDER_CHOICES)
    date_naissance = models.DateField()
    ville          = models.CharField(max_length=100)
    actif          = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} ({self.groupe_sanguin})"

    class Meta:
        verbose_name        = "Donneur"
        verbose_name_plural = "Donneurs"


class Hopital(models.Model):

    user = models.OneToOneField(
                    User,
                    on_delete=models.CASCADE,
                    related_name='hopital'
                 )
    nom        = models.CharField(max_length=200)
    adresse    = models.TextField()
    ville      = models.CharField(max_length=100)
    agrement   = models.CharField(max_length=100, unique=True)
    valide     = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name        = "Hopital"
        verbose_name_plural = "Hopitaux"
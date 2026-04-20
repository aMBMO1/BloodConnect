from django.db import models
from core.models import Donneur, Hopital


class Don(models.Model):

    donneur    = models.ForeignKey(
                    Donneur,
                    on_delete=models.CASCADE,
                    related_name='dons'
                 )
    hopital    = models.ForeignKey(
                    Hopital,
                    on_delete=models.CASCADE,
                    related_name='dons_recus'
                 )
    date_don   = models.DateField()
    notes      = models.TextField(blank=True)
    valide     = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Don de {self.donneur.user.username} - {self.date_don}"

    class Meta:
        verbose_name        = "Don"
        verbose_name_plural = "Dons"
        ordering            = ['-date_don']


class DemandeUrgente(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
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

    hopital        = models.ForeignKey(
                        Hopital,
                        on_delete=models.CASCADE,
                        related_name='demandes'
                     )
    groupe_sanguin = models.CharField(max_length=3, choices=BLOOD_TYPES)
    quantite       = models.PositiveIntegerField()
    delai          = models.DateField()
    statut         = models.CharField(
                        max_length=20,
                        choices=STATUS_CHOICES,
                        default='active'
                     )
    description    = models.TextField()
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.groupe_sanguin} - {self.hopital.nom}"

    class Meta:
        verbose_name        = "Demande Urgente"
        verbose_name_plural = "Demandes Urgentes"
        ordering            = ['-created_at']


class ReponseAppel(models.Model):

    STATUS_CHOICES = [
        ('interested', 'Interested'),
        ('confirmed',  'Confirmed'),
        ('declined',   'Declined'),
    ]

    donneur      = models.ForeignKey(
                        Donneur,
                        on_delete=models.CASCADE,
                        related_name='reponses'
                   )
    demande      = models.ForeignKey(
                        DemandeUrgente,
                        on_delete=models.CASCADE,
                        related_name='reponses'
                   )
    date_reponse = models.DateTimeField(auto_now_add=True)
    statut       = models.CharField(
                        max_length=20,
                        choices=STATUS_CHOICES,
                        default='interested'
                   )

    def __str__(self):
        return f"{self.donneur.user.username} - {self.demande}"

    class Meta:
        verbose_name        = "Reponse Appel"
        verbose_name_plural = "Reponses Appel"
        ordering            = ['-date_reponse']
        unique_together     = ('donneur', 'demande')
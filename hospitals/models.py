from django.db import models
from core.models import Hopital, Donneur


class Campagne(models.Model):

    hopital         = models.ForeignKey(
                        Hopital,
                        on_delete=models.CASCADE,
                        related_name='campagnes'
                      )
    nom             = models.CharField(max_length=200)
    date            = models.DateField()
    lieu            = models.CharField(max_length=200)
    groupes_cibles  = models.CharField(max_length=100)
    capacite_totale = models.PositiveIntegerField()
    created_at      = models.DateTimeField(auto_now_add=True)

    def places_restantes(self):
        return self.capacite_totale - self.inscriptions.count()

    def est_pleine(self):
        return self.inscriptions.count() >= self.capacite_totale

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name        = "Campagne"
        verbose_name_plural = "Campagnes"
        ordering            = ['-date']


class Inscription(models.Model):

    campagne         = models.ForeignKey(
                            Campagne,
                            on_delete=models.CASCADE,
                            related_name='inscriptions'
                       )
    donneur          = models.ForeignKey(
                            Donneur,
                            on_delete=models.CASCADE,
                            related_name='inscriptions'
                       )
    creneau_horaire  = models.TimeField()
    date_inscription = models.DateTimeField(auto_now_add=True)
    present          = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.donneur.user.username} - {self.campagne.nom}"

    class Meta:
        verbose_name        = "Inscription"
        verbose_name_plural = "Inscriptions"
        unique_together     = ('campagne', 'donneur')
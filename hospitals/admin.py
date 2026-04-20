from django.contrib import admin
from .models import Campagne, Inscription


@admin.register(Campagne)
class CampagneAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'hopital', 'date', 'lieu', 'capacite_totale']
    list_filter   = ['date']
    search_fields = ['nom', 'hopital__nom']


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display  = ['donneur', 'campagne', 'creneau_horaire', 'present']
    list_filter   = ['present']
    search_fields = ['donneur__user__username']
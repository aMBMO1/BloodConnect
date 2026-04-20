from django.contrib import admin
from .models import Don, DemandeUrgente, ReponseAppel


@admin.register(Don)
class DonAdmin(admin.ModelAdmin):
    list_display  = ['donneur', 'hopital', 'date_don', 'valide']
    list_filter   = ['valide', 'date_don']
    search_fields = ['donneur__user__username', 'hopital__nom']


@admin.register(DemandeUrgente)
class DemandeUrgenteAdmin(admin.ModelAdmin):
    list_display  = ['hopital', 'groupe_sanguin', 'quantite', 'delai', 'statut']
    list_filter   = ['groupe_sanguin', 'statut']
    search_fields = ['hopital__nom']


@admin.register(ReponseAppel)
class ReponseAppelAdmin(admin.ModelAdmin):
    list_display  = ['donneur', 'demande', 'date_reponse', 'statut']
    list_filter   = ['statut']
    search_fields = ['donneur__user__username']
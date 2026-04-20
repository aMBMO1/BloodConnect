from django.contrib import admin
from .models import Donneur, Hopital


@admin.register(Donneur)
class DonneurAdmin(admin.ModelAdmin):
    list_display  = ['user', 'groupe_sanguin', 'sexe', 'ville', 'actif']
    list_filter   = ['groupe_sanguin', 'ville', 'actif', 'sexe']
    search_fields = ['user__username', 'ville']


@admin.register(Hopital)
class HopitalAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'ville', 'agrement', 'valide']
    list_filter   = ['valide', 'ville']
    search_fields = ['nom', 'agrement']
    actions       = ['validate_hospitals']

    def validate_hospitals(self, request, queryset):
        queryset.update(valide=True)
        self.message_user(request, "Selected hospitals validated!")
    validate_hospitals.short_description = "Validate selected hospitals"
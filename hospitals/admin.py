from django.contrib import admin
from .models import Campaign, Registration


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display  = ['name', 'hospital', 'date', 'location', 'total_capacity']
    list_filter   = ['date']
    search_fields = ['name', 'hospital__name']


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display  = ['donor', 'campaign', 'time_slot', 'present']
    list_filter   = ['present']
    search_fields = ['donor__user__username']
from django.contrib import admin
from .models import Donation, UrgentRequest, AppealResponse


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display  = ['donor', 'hospital', 'donation_date', 'validated']
    list_filter   = ['validated', 'donation_date']
    search_fields = ['donor__user__username', 'hospital__name']


@admin.register(UrgentRequest)
class UrgentRequestAdmin(admin.ModelAdmin):
    list_display  = ['hospital', 'blood_type', 'quantity', 'deadline', 'status']
    list_filter   = ['blood_type', 'status']
    search_fields = ['hospital__name']


@admin.register(AppealResponse)
class AppealResponseAdmin(admin.ModelAdmin):
    list_display  = ['donor', 'request', 'response_date', 'status']
    list_filter   = ['status']
    search_fields = ['donor__user__username']
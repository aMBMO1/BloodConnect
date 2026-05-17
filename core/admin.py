from django.contrib import admin
from .models import Donor, Hospital


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display  = ['user', 'blood_type', 'gender', 'city', 'active']
    list_filter   = ['blood_type', 'city', 'active', 'gender']
    search_fields = ['user__username', 'city']


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display  = ['name', 'city', 'approval', 'validated']
    list_filter   = ['validated', 'city']
    search_fields = ['name', 'approval']
    actions       = ['validate_hospitals']

    def validate_hospitals(self, request, queryset):
        queryset.update(validated=True)
        self.message_user(request, "Selected hospitals validated!")
    validate_hospitals.short_description = "Validate selected hospitals"
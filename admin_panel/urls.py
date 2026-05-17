# admin_panel/urls.py
from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('',                                        views.dashboard,             name='dashboard'),
    path('hospitals/',                             views.hospitals_list,        name='hospitals_list'),
    path('hospitals/<int:hospital_id>/validate/',  views.validate_hospital,     name='validate_hospital'),
    path('hospitals/<int:hospital_id>/reject/',    views.reject_hospital,       name='reject_hospital'),
    path('donors/',                                views.donors_list,           name='donors_list'),
    path('donors/export-csv/',                     views.export_donors_csv,     name='export_donors_csv'),
path('donations/<int:donation_id>/validate/',  views.validate_donation, name='validate_donation'),
    path('campaigns/',                             views.campaigns_list,        name='campaigns_list'),
]
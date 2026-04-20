from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/',
         views.dashboard,
         name='dashboard'),

    path('hopitaux/',
         views.hopitaux_list,
         name='hopitaux_list'),

    path('hopitaux/<int:hopital_id>/valider/',
         views.valider_hopital,
         name='valider_hopital'),

    path('hopitaux/<int:hopital_id>/rejeter/',
         views.rejeter_hopital,
         name='rejeter_hopital'),

    path('donneurs/',
         views.donneurs_list,
         name='donneurs_list'),


]
from django.urls import path
from . import views

app_name = 'hospitals'

urlpatterns = [
    path('dashboard/',
         views.dashboard,
         name='dashboard'),

    path('demandes/creer/',
         views.creer_demande,
         name='creer_demande'),

    path('demandes/<int:demande_id>/',
         views.voir_demande,
         name='voir_demande'),

    path('demandes/<int:demande_id>/modifier/',
         views.modifier_demande,
         name='modifier_demande'),

    path('demandes/<int:demande_id>/cloturer/',
         views.cloturer_demande,
         name='cloturer_demande'),

    path('campagnes/',
         views.liste_campagnes,
         name='liste_campagnes'),

    path('campagnes/creer/',
         views.creer_campagne,
         name='creer_campagne'),

    path('campagnes/<int:campagne_id>/',
         views.detail_campagne,
         name='detail_campagne'),

    path('campagnes/<int:campagne_id>/inscrire/',
         views.inscrire_campagne,
         name='inscrire_campagne'),
]
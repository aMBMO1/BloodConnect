from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('dashboard/',
         views.dashboard,
         name='dashboard'),

    path('mes-dons/',
         views.mes_dons,
         name='mes_dons'),

    path('enregistrer/',
         views.enregistrer_don,
         name='enregistrer_don'),

    path('appels-urgents/',
         views.appels_urgents,
         name='appels_urgents'),

    path('repondre/<int:demande_id>/',
         views.repondre_appel,
         name='repondre_appel'),

    path('mes-reponses/',
         views.mes_reponses,
         name='mes_reponses'),
]
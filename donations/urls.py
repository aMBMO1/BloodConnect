from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('dashboard/',                        views.dashboard,        name='dashboard'),
    path('mes-dons/',                         views.mes_dons,         name='mes_dons'),
    path('enregistrer/',                      views.enregistrer_don,  name='enregistrer_don'),
    path('mes-dons/<int:don_id>/modifier/',   views.modifier_don,     name='modifier_don'),   # ✅ new
    path('mes-dons/<int:don_id>/supprimer/',  views.supprimer_don,    name='supprimer_don'),  # ✅ new
    path('appels-urgents/',                   views.appels_urgents,   name='appels_urgents'),
    path('repondre/<int:demande_id>/',        views.repondre_appel,   name='repondre_appel'),
    path('mes-reponses/',                     views.mes_reponses,     name='mes_reponses'),
]
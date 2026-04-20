from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',
         views.home,
         name='home'),

    path('register/donneur/',
         views.register_donneur,
         name='register_donneur'),

    path('register/hopital/',
         views.register_hopital,
         name='register_hopital'),



    path('profile/',
         views.profile,
         name='profile'),
]
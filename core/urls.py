from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',
         views.home,
         name='home'),

    path('register/donor/',
         views.register_donor,
         name='register_donor'),

    path('register/hospital/',
         views.register_hospital,
         name='register_hospital'),

    path('login/',
         views.user_login,
         name='login'),

    path('logout/',
         views.user_logout,
         name='logout'),

    path('profile/',
         views.profile,
         name='profile'),
    path('profile/toggle-active/',
         views.toggle_active,
         name='toggle_active'),
]
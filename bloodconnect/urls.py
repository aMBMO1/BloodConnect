from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/',       admin.site.urls),
    path('',             include('core.urls')),
    path('donations/',   include('donations.urls')),
    path('hospitals/',   include('hospitals.urls')),
    path('admin-panel/', include('admin_panel.urls')),
]
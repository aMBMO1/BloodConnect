from django.urls import path
from . import views

app_name = 'hospitals'

urlpatterns = [
    path('dashboard/',                                  views.dashboard,            name='dashboard'),
    path('requests/create/',                            views.create_request,       name='create_request'),
    path('requests/<int:request_id>/',                  views.view_request,         name='view_request'),
    path('requests/<int:request_id>/modify/',           views.modify_request,       name='modify_request'),
    path('requests/<int:request_id>/close/',            views.close_request,        name='close_request'),
    path('campaigns/',                                  views.campaign_list,        name='campaign_list'),
    path('campaigns/create/',                           views.create_campaign,      name='create_campaign'),
    path('campaigns/<int:campaign_id>/',                views.campaign_detail,      name='campaign_detail'),
    path('campaigns/<int:campaign_id>/register/',       views.register_campaign,    name='register_campaign'),
    path('campaigns/<int:campaign_id>/modify/',         views.modify_campaign,      name='modify_campaign'),
    path('campaigns/<int:campaign_id>/delete/',         views.delete_campaign,      name='delete_campaign'),
]
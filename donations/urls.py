from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('dashboard/',                               views.dashboard,           name='dashboard'),
    path('my-donations/',                            views.my_donations,        name='my_donations'),
    path('register/',                                views.register_donation,   name='register_donation'),
    path('my-donations/<int:donation_id>/modify/',   views.modify_donation,     name='modify_donation'),
    path('my-donations/<int:donation_id>/delete/',   views.delete_donation,     name='delete_donation'),
    path('urgent-appeals/',                          views.urgent_appeals,      name='urgent_appeals'),
    path('respond/<int:request_id>/',                views.respond_to_appeal,   name='respond_to_appeal'),
    path('my-responses/',                            views.my_responses,        name='my_responses'),
]
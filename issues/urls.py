from django.urls import path
from .views import IssueCreateView
from django.views.generic import TemplateView

urlpatterns = [
    path('report/', IssueCreateView.as_view(), name='report_issue'),
    path('thanks/', TemplateView.as_view(template_name="issues/thanks.html"), name='issue_thanks'),
]

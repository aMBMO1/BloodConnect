# issues/urls.py
from django.urls import path
from .views import IssueCreateView, IssueListView
from django.views.generic import TemplateView

app_name = "issues"   # <-- add this line

urlpatterns = [
    path('report/', IssueCreateView.as_view(), name='report_issue'),
    path('list/', IssueListView.as_view(), name='issue_list'),
    path('thanks/', TemplateView.as_view(template_name="issues/thanks.html"), name='issue_thanks'),
]

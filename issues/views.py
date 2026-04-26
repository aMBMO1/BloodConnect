from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Issue

class IssueCreateView(CreateView):
    model = Issue
    fields = ['title', 'description', 'user_email']
    template_name = 'issues/report_issue.html'
    success_url = reverse_lazy('issue_thanks')



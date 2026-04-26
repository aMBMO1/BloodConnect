from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import Issue

class IssueCreateView(CreateView):
    model = Issue
    fields = ['title', 'description', 'user_email']
    template_name = 'issues/report_issue.html'
    success_url = reverse_lazy('issue_thanks')

class IssueListView(ListView):
    model = Issue
    template_name = 'issues/issue_list.html'
    context_object_name = 'issues'
    ordering = ['-created_at']
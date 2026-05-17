from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import Issue
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

@method_decorator(staff_member_required, name='dispatch')
class IssueListView(ListView):
    model = Issue
    template_name = 'issues/issue_list.html'
    context_object_name = 'issues'
    ordering = ['-created_at']

class IssueCreateView(CreateView):
    model = Issue
    fields = ['title', 'description', 'user_email']
    template_name = 'issues/report_issue.html'
    success_url = reverse_lazy('issues:issue_thanks')
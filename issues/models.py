from django.db import models

class Issue(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.title

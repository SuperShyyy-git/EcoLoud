from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

from django.conf import settings

class Campaign(models.Model):
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Description', config_name='extends')
    image = models.ImageField(upload_to='campaigns/', blank=True, null=True)
    goal = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # URL helpers for templates
    def get_edit_url(self):
        return reverse('campaigns:campaign_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('campaigns:campaign_delete', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('campaigns:campaign_detail', kwargs={'pk': self.pk})


class CampaignSuggestion(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    reason = models.TextField(help_text="Why should we run this campaign?")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Membership(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('active', _('Active')),
        ('rejected', _('Rejected')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships', verbose_name=_("User"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name=_("Status"))
    start_date = models.DateField(null=True, blank=True, verbose_name=_("Start Date"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("End Date"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"{self.user} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Membership")
        verbose_name_plural = _("Memberships")

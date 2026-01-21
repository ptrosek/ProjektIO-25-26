from django.db import models
from django.utils.translation import gettext_lazy as _
from appointment.models import Service, Appointment
from django.contrib.auth import get_user_model

User = get_user_model()

class ClassRegistration(models.Model):
    """
    Tracks which users have registered for a specific Group Class instance (Appointment).
    Keeping this for future use or dormant, as removing it requires migration cleanup.
    Actually, prompt said "delete all overrides for Classes".
    If I delete this model, I need to clean up migrations or squash them.
    Since this is MVP dev, I will delete it too to be clean.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='class_registrations', verbose_name=_("User"))
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='registrations', verbose_name=_("Appointment"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Registered At"))

    class Meta:
        unique_together = ('user', 'appointment')
        verbose_name = _("Class Registration")
        verbose_name_plural = _("Class Registrations")
    
    def __str__(self):
        return f"{self.user} -> {self.appointment}"

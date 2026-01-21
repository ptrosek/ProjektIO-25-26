from django.db.models.signals import pre_save
from django.dispatch import receiver
from appointment.models import Appointment
from memberships.models import Membership
from datetime import date

@receiver(pre_save, sender=Appointment)
def apply_membership_discount(sender, instance, **kwargs):
    """
    If the user has an active membership, the appointment is free.
    """
    if not instance.client:
        return

    # Check for active membership
    # Active = status 'active' AND today is between start and end date
    today = date.today()
    has_membership = Membership.objects.filter(
        user=instance.client,
        status='active',
        start_date__lte=today,
        end_date__gte=today
    ).exists()
    
    if has_membership:
        instance.amount_to_pay = 0
        instance.paid = True

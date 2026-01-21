from django.db.models.signals import pre_save
from django.dispatch import receiver
from appointment.models import Appointment
from memberships.models import Membership
from django.utils import timezone

@receiver(pre_save, sender=Appointment)
def apply_membership_discount(sender, instance, **kwargs):
    if instance.client:
        today = timezone.now().date()
        # Find active membership
        memberships = Membership.objects.filter(user=instance.client, status='active')

        has_active = False
        for m in memberships:
            start = m.start_date
            end = m.end_date
            if start and start > today:
                continue
            if end and end < today:
                continue
            has_active = True
            break

        if has_active:
            instance.amount_to_pay = 0
            instance.paid = True

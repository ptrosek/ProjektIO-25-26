from django.contrib import admin
from django.utils.translation import gettext as _
from .models import Membership
import threading
from core_fitness.tasks import send_welcome_email

@admin.action(description=_("Approve selected memberships"))
def approve_memberships(modeladmin, request, queryset):
    for membership in queryset:
        if membership.status != 'active':
            membership.status = 'active'
            # Set default dates if needed, e.g., start today, end in 30 days
            # For MVP, we assume Admin sets dates or we handle it here.
            import datetime
            if not membership.start_date:
                membership.start_date = datetime.date.today()
            if not membership.end_date:
                membership.end_date = datetime.date.today() + datetime.timedelta(days=30)
            
            membership.save()
            
            # Trigger Welcome Email Task
            try:
                # Direct call to threading function
                send_welcome_email(user_email=membership.user.email)
            except Exception as e:
                pass

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'start_date', 'end_date', 'created_at')
    list_filter = ('status',)
    actions = [approve_memberships]

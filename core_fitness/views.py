import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from appointment.models import Appointment, Service
from .models import ClassRegistration

def service_list(request):
    """
    List all services with links to book them.
    """
    services = Service.objects.all()
    return render(request, 'core_fitness/service_list.html', {'services': services})

@login_required
def my_bookings(request):
    """
    List bookings for the logged-in user.
    """
    # 1. Direct appointments
    direct_appointments = Appointment.objects.filter(client=request.user).order_by('-appointment_request__date')
    
    context = {
        'direct_appointments': direct_appointments,
    }
    return render(request, 'core_fitness/my_bookings.html', context)

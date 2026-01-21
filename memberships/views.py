from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Membership

@login_required
def request_membership(request):
    # Check if user already has a pending or active membership
    existing = Membership.objects.filter(user=request.user, status__in=['pending', 'active']).first()

    if request.method == 'POST':
        if existing:
            messages.info(request, "You already have a membership application in progress or active.")
            return redirect('home')

        Membership.objects.create(user=request.user, status='pending')
        messages.success(request, "Membership requested successfully.")
        return redirect('home')

    return render(request, 'memberships/request.html', {'existing': existing})

@staff_member_required
def staff_membership_list(request):
    memberships = Membership.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'memberships/staff_list.html', {'memberships': memberships})

@staff_member_required
def update_membership_status(request, pk):
    membership = get_object_or_404(Membership, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            membership.status = 'active'
            membership.save()
            messages.success(request, f"Membership for {membership.user} approved.")
        elif action == 'reject':
            membership.status = 'rejected'
            membership.save()
            messages.success(request, f"Membership for {membership.user} rejected.")
    return redirect('staff_membership_list')

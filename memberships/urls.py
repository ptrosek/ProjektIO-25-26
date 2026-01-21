from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.request_membership, name='request_membership'),
    path('staff/list/', views.staff_membership_list, name='staff_membership_list'),
    path('staff/update/<int:pk>/', views.update_membership_status, name='update_membership_status'),
]

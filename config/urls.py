from django.contrib import admin
from django.urls import path, include
from core_fitness.views import service_list, my_bookings

urlpatterns = [
    path('admin/', admin.site.urls),
    # Map root URL to service list
    path('', service_list, name='home'),
    # Map appointments/ root to service list
    path('appointments/', service_list, name='service_list'),
    path('appointments/my-bookings/', my_bookings, name='my_bookings'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('appointments/', include('appointment.urls')),
]

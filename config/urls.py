from django.contrib import admin
from django.urls import path, include
from core_fitness.views import service_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', service_list, name='home'),
    path('core/', include('core_fitness.urls')),
    path('memberships/', include('memberships.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # Keep third-party appointment urls
    path('appointments/', include('appointment.urls')),
]

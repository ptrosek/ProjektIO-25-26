from django.apps import AppConfig
from django.conf import settings

class CoreFitnessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_fitness'

    def ready(self):
        # Apply Monkey Patches
        from appointment import views
        from appointment.models import Appointment
        from .monkey_patches import appointment_save_wrapper
        
        # Patch Appointment.save
        Appointment.save = appointment_save_wrapper(Appointment.save)
        
        # Connect Signals
        import core_fitness.signals

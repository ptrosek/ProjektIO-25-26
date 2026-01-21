from appointment.models import Appointment

# Monkey Patch for Appointment.save
def appointment_save_wrapper(original_save):
    def wrapper(self, *args, **kwargs):
        original_save(self, *args, **kwargs)     
    return wrapper

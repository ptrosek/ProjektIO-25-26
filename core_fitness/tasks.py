import threading
import time
from django.core.mail import send_mail

def send_welcome_email(user_email):
    """
    Sends a welcome email to the user using a background thread.
    """
    def _send():
        print(f"Starting background task: Sending email to {user_email}")
        # Simulate delay
        time.sleep(2)
        
        send_mail(
            subject="Welcome to Studio Fitness!",
            message="Your membership has been approved! You can now book classes for free.",
            from_email="admin@studiofitness.com",
            recipient_list=[user_email],
            fail_silently=False,
        )
        print(f"Finished background task: Email sent to {user_email}")

    thread = threading.Thread(target=_send)
    thread.start()

# Compatibility wrapper to mimic .enqueue() if needed, or we just call it directly.
# The admin action calls send_welcome_email.enqueue(...) based on my previous code.
# Let's fix the admin action to call send_welcome_email(user_email) directly.

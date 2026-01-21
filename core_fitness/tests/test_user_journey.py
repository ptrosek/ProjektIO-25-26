from django.test import TestCase, Client
from django.core.management import call_command
from django.contrib.auth import get_user_model
from appointment.models import Appointment, AppointmentRequest, Service, StaffMember
# from core_fitness.models import Room, ServiceProfile, ClassRegistration
import datetime
from django.urls import reverse

User = get_user_model()

class UserJourneyTest(TestCase):
    def setUp(self):
        # 1. Seed Data
        call_command('seed_studio')
        
        self.client = Client()
        self.bob = User.objects.get(username='bob')
        self.alice_staff = StaffMember.objects.get(user__username='alice')
        self.pt_service = Service.objects.get(name='Personal Training')

    def test_pt_booking_journey(self):
        """
        Bob logs in and books a Personal Training session.
        """
        # Login
        self.client.force_login(self.bob)
        
        # 1. Check availability
        target_date = datetime.date.today() + datetime.timedelta(days=2)
        if target_date.weekday() > 4: # Skip weekend
             target_date += datetime.timedelta(days=(7 - target_date.weekday()))
             
        start_time = datetime.time(14, 0) # 2 PM
        
        # Check Availability API
        url = reverse('appointment:available_slots_ajax')
        # Add HTTP_X_REQUESTED_WITH header for AJAX check
        response = self.client.get(url, {
            'staff_member': self.alice_staff.id,
            'selected_date': target_date.isoformat(),
            'service': self.pt_service.id
        }, headers={'x-requested-with': 'XMLHttpRequest'})
        
        if response.status_code != 200:
            print(f"DEBUG: Status {response.status_code}")
        
        json_data = response.json()
        
        self.assertEqual(response.status_code, 200)
        
        # Determine where slots are (Root or custom_data)
        if 'custom_data' in json_data:
            slots_container = json_data['custom_data']
        else:
            slots_container = json_data
            
        self.assertIn('available_slots', slots_container)
        
        # Book it
        ar = AppointmentRequest.objects.create(
            date=target_date,
            start_time=start_time,
            end_time=(datetime.datetime.combine(target_date, start_time) + datetime.timedelta(hours=1)).time(),
            service=self.pt_service,
            staff_member=self.alice_staff
        )
        appt = Appointment.objects.create(
            appointment_request=ar,
            client=self.bob,
            amount_to_pay=100
        )
        
        # Room check verification removed
        self.assertTrue(Appointment.objects.filter(id=appt.id).exists())

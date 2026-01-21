from django.test import TestCase
from django.contrib.auth import get_user_model
from appointment.models import Appointment, AppointmentRequest, Service, StaffMember, Config
# from core_fitness.models import Room, ServiceProfile, ClassRegistration
# from core_fitness.availability import check_room_availability
from memberships.models import Membership
import datetime
from django.utils import timezone

User = get_user_model()

# RoomAvailabilityTests removed

class MembershipDiscountTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(name="PT", duration=datetime.timedelta(hours=1), price=100)
        self.user = User.objects.create_user(username="member", email="member@example.com")
        self.staff_user = User.objects.create_user(username="staff", email="staff@example.com")
        self.staff = StaffMember.objects.create(user=self.staff_user)
        Config.objects.create(slot_duration=30, lead_time=datetime.time(9,0), finish_time=datetime.time(17,0))

    def test_discount_applied(self):
        # Active membership
        Membership.objects.create(
            user=self.user, status='active', 
            start_date=datetime.date.today(), 
            end_date=datetime.date.today() + datetime.timedelta(days=30)
        )
        
        ar = AppointmentRequest.objects.create(
            date=datetime.date.today(), start_time=datetime.time(12, 0), end_time=datetime.time(13, 0),
            service=self.service, staff_member=self.staff
        )
        
        # Create appointment - signal should trigger
        appt = Appointment(appointment_request=ar, client=self.user)
        appt.save()
        
        self.assertEqual(appt.amount_to_pay, 0)
        self.assertTrue(appt.paid)

    def test_no_discount_for_pending(self):
        Membership.objects.create(user=self.user, status='pending')
        
        ar = AppointmentRequest.objects.create(
            date=datetime.date.today(), start_time=datetime.time(14, 0), end_time=datetime.time(15, 0),
            service=self.service, staff_member=self.staff
        )
        
        appt = Appointment(appointment_request=ar, client=self.user)
        appt.save()
        
        # So it should be 100
        self.assertEqual(appt.amount_to_pay, 100)

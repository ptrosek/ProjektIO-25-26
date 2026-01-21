import datetime
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from appointment.models import Service

User = get_user_model()

class CoreFitnessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        # Fix: Pass timedelta for duration
        self.service = Service.objects.create(
            name="Test Service",
            duration=datetime.timedelta(hours=1),
            price=100
        )

    def test_service_list(self):
        response = self.client.get('/core/services/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Service")
        self.assertContains(response, "Book Now")

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Service")

    def test_my_bookings_requires_login(self):
        response = self.client.get('/core/my-bookings/')
        self.assertEqual(response.status_code, 302) # Redirects to login

    def test_my_bookings(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get('/core/my-bookings/')
        self.assertEqual(response.status_code, 200)

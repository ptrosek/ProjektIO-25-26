from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from memberships.models import Membership

User = get_user_model()

class MembershipTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.staff_user = User.objects.create_user(username='staffuser', password='password', is_staff=True)
        self.staff_user.save()

    def test_request_membership(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/memberships/request/')
        self.assertEqual(response.status_code, 302) # Redirects to home
        self.assertTrue(Membership.objects.filter(user=self.user, status='pending').exists())

    def test_staff_approve_membership(self):
        membership = Membership.objects.create(user=self.user, status='pending')
        self.client.login(username='staffuser', password='password')
        response = self.client.post(f'/memberships/staff/update/{membership.pk}/', {'action': 'approve'})
        self.assertEqual(response.status_code, 302) # Redirects to list
        membership.refresh_from_db()
        self.assertEqual(membership.status, 'active')

    def test_staff_reject_membership(self):
        membership = Membership.objects.create(user=self.user, status='pending')
        self.client.login(username='staffuser', password='password')
        response = self.client.post(f'/memberships/staff/update/{membership.pk}/', {'action': 'reject'})
        self.assertEqual(response.status_code, 302)
        membership.refresh_from_db()
        self.assertEqual(membership.status, 'rejected')

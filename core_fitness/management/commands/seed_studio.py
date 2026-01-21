import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from appointment.models import Service, StaffMember, WorkingHours, Config, Appointment, AppointmentRequest
# from core_fitness.models import Room, ServiceProfile
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with example data for Studio Fitness'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # 1. Config
        if not Config.objects.exists():
            Config.objects.create(
                slot_duration=60,
                lead_time=datetime.time(8, 0),
                finish_time=datetime.time(20, 0),
                appointment_buffer_time=0
            )

        # 2. Users & Staff
        # Admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        
        # Instructor Alice
        alice_user, created = User.objects.get_or_create(
            username='alice', 
            defaults={'email': 'alice@studio.com', 'first_name': 'Alice', 'last_name': 'Instructor'}
        )
        if created:
            alice_user.set_password('staffpass')
            alice_user.save()
        
        alice_staff, created = StaffMember.objects.get_or_create(user=alice_user)
        alice_staff.lead_time = datetime.time(9, 0)
        alice_staff.finish_time = datetime.time(17, 0)
        alice_staff.save()

        # Set Working Hours for Alice (Mon-Fri)
        for day in range(0, 5): # 0=Monday, 4=Friday
            WorkingHours.objects.get_or_create(
                staff_member=alice_staff,
                day_of_week=day,
                defaults={'start_time': datetime.time(9, 0), 'end_time': datetime.time(17, 0)}
            )

        # Client Bob
        bob, created = User.objects.get_or_create(
            username='bob', 
            defaults={'email': 'bob@client.com', 'first_name': 'Bob', 'last_name': 'Client'}
        )
        if created:
            bob.set_password('clientpass')
            bob.save()

        # 3. Services
        # Personal Training
        pt_service, created = Service.objects.get_or_create(
            name='Personal Training',
            defaults={
                'duration': datetime.timedelta(minutes=60),
                'price': 100.00,
                'description': '1-on-1 Session'
            }
        )
        alice_staff.services_offered.add(pt_service)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

from django.core.management.base import BaseCommand
from auths.models import PhoneNumber, UserAddress, User  # Adjust this based on your app name
from django.utils.timezone import now
import random


class Command(BaseCommand):
    help = "Create 10 users (1 admin + 9 regular users) with phone numbers and addresses."

    def handle(self, *args, **kwargs):
        # Create an Admin User
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="Admin@123",
                first_name="Admin",
                last_name="User",
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Created admin user: {admin_user.username}"))
        else:
            self.stdout.write(self.style.WARNING("⚠️ Admin user already exists."))

        # Generate 9 Regular Users
        for i in range(9):
            username = f"user{i + 1}"
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f"⚠️ User {username} already exists. Skipping."))
                continue

            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="User@123",
                first_name=f"First{i + 1}",
                last_name=f"Last{i + 1}",
                date_of_birth=now().date(),
                gender=random.choice(["Male", "Female", "Other"]),
                preferred_language=random.choice(["en", "vi"]),
            )

            # Add a phone number
            phone = PhoneNumber.objects.create(
                user=user,
                phone_number=f"+8409876543{i + 1}",
                is_primary=True,
                is_phone_verified=True,
            )
            user.default_phone_number = phone
            user.save()

            # Add an address
            address = UserAddress.objects.create(
                user=user,
                phone_number=phone,
                address_line1=f"123 Street {i + 1}",
                city="Hanoi",
                state="Vietnam",
                postal_code="100000",
                country="VN",
                latitude=21.0285,
                longitude=105.8542,
                is_default=True,
            )
            user.default_address = address
            user.save()

            self.stdout.write(self.style.SUCCESS(f"✅ Created user: {username}"))

        self.stdout.write(self.style.SUCCESS("🎉 Successfully created 10 users!"))

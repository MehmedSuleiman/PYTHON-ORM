import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Astronaut, Spacecraft, Mission
from datetime import date

# Clear existing data
Astronaut.objects.all().delete()
Spacecraft.objects.all().delete()
Mission.objects.all().delete()

print("Creating Astronauts...")
# Astronauts
john = Astronaut.objects.create(
    name="John Deer",
    phone_number="853967",
    is_active=True,
    date_of_birth=date(1980, 1, 1),
    spacewalks=3
)

jane = Astronaut.objects.create(
    name="Jane Smith",
    phone_number="123456",
    is_active=True,
    date_of_birth=date(1985, 5, 15),
    spacewalks=1
)

josie = Astronaut.objects.create(
    name="Josie Stam",
    phone_number="111111",
    is_active=False,
    date_of_birth=date(1990, 3, 12),
    spacewalks=0
)

print("Creating Spacecrafts...")
# Spacecrafts
explorer_i = Spacecraft.objects.create(
    name="Explorer I",
    manufacturer="SpaceTech Inc.",
    capacity=5,
    weight=12000.5,
    launch_date=date(2022, 1, 1)
)

explorer_ii = Spacecraft.objects.create(
    name="Explorer II",
    manufacturer="SpaceX",
    capacity=2,
    weight=10000.2,
    launch_date=date(2023, 5, 1)
)

print("Creating Missions...")
# Missions
mission1 = Mission.objects.create(
    name="Moon Landing",
    status=Mission.Status.PLANNED,
    description="Landing on the moon",
    spacecraft=explorer_i,
    commander=john,
    launch_date=date(2024, 10, 10)
)
mission1.astronauts.add(john, jane)

mission2 = Mission.objects.create(
    name="Moon Landing2",
    status=Mission.Status.COMPLETED,
    description="Landing on the moon",
    spacecraft=explorer_i,
    commander=josie,
    launch_date=date(2024, 3, 1)
)
mission2.astronauts.add(jane, josie)

print("Test data inserted successfully!")

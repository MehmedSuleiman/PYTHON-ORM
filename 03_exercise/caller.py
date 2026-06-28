import os
from decimal import Decimal
from typing import Optional

import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom


# Create queries within functions

def create_pet(name: str, species: str) -> str:
    # pet = Pet.objects.create(name=name, species=species,)
    # return f"{pet.name} is a very cute {pet.species}!"

    pet = Pet.objects.create(
        name=name,
        species=species,
    )
    return f"{pet.name} is a very cute {pet.species}!"

def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
    )
    return f"The artifact {name} is {age} years old!"

def rename_artifact(artifact: Artifact, new_name: str) -> None:
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()

def delete_all_artifacts()-> None:
    Artifact.objects.all().delete()

def show_all_locations()-> str:
    locations = Location.objects.all()
    for loc in locations:
        print(f"{loc.name} has a population of {loc.population}!")

def new_capital() -> None:
    loc = Location.objects.first
    loc.is_capital = True
    loc.save()

def get_capital() -> QuerySet:
    return Location.objects.filter(is_capital = True).values("name")


def delete_first_location() -> None:
    Location.objects.first().delete()

def apply_discount()-> None:
    for car in Car.objects.all():
        # 2008 -> "2008" -> 2 + 0 + 0 + 8 -> 10 / 100 -> 0.10
        percentage_off = Decimal(str(sum(int(d) for d in str(car.year)) / 100))
        discount = car.price * percentage_off  # 10 000 * 0.10 -> 1 000
        car.price_with_discount = car.price - discount
        car.save()

def get_recent_cars() -> QuerySet:
    return Car.objects.filter(year__gt= 2020).values("model", "price_with_discount")

def delete_last_car() -> None:
    Car.objects.last().delete()

def show_unfinished_tasks()-> str:
    unfinished = Task.objects.filter(is_finished = False)
    for task in unfinished:
        print(f"Task - {task.title} needs to be done until {task.due_date}!")

def complete_odd_tasks():
    tasks = Task.objects.all()
    odd_tasks = []

    for task in tasks:
        if task.id % 2 != 0:
            task.completed = True
            odd_tasks.append(task)

    Task.objects.bulk_update(odd_tasks, ["is_finished"])

def encode_and_replace(text: str, task_title: str) -> None:
    encoded_text = ''.join(chr(ord(l) - 3) for l in text)

    Task.objects.filter(title=task_title).update(description=encoded_text)


def get_deluxe_rooms() -> str:
    d_rooms = HotelRoom.objects.filter(room_type = HotelRoom.RoomType.DELUXE)
    even_id_rooms = [r for r in d_rooms if r.id % 2 == 0]

    return '\n'.join(
        f"Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!"
        for r in even_id_rooms
    )

def increase_room_capacity() -> None:
    reserved_rooms = HotelRoom.objects.filter(is_reserved=True).order_by('id')
    previous_room: Optional[HotelRoom] = None
    updated_rooms = []

    for r in reserved_rooms:
        if previous_room:
            r.capacity += previous_room.capacity
        else:
            r.capacity += r.id

        previous_room = r
        updated_rooms.append(r)

    HotelRoom.objects.bulk_update(updated_rooms, ["capacity"])

def delete_last_room() -> None:
    room = HotelRoom.objects.last()

    if not room.is_reserved:
        room.delete()


def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()



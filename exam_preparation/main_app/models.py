from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from main_app.managers import AstronautManager
from main_app.validators import phone_validator


# Create your models here.
class UpdatedTimeStamp(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)

class LaunchTimeStamp(models.Model):
    class Meta:
        abstract = True

    launch_date = models.DateField(auto_now_add=True)


class Astronaut(UpdatedTimeStamp):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )

    phone_number = models.CharField(
        max_length= 15,
        unique=True,
        validators=[
            phone_validator
        ]
    )

    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank= True)
    spacewalks = models.PositiveIntegerField(default=0)

    objects = AstronautManager()

    @property
    def status(self):
        return "Active" if self.is_active else "Inactive"

class Spacecraft(UpdatedTimeStamp, LaunchTimeStamp):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )
    manufacturer = models.CharField(
        max_length=100,
    )

    capacity = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )

    weight = models.FloatField(
        validators=[
            MinValueValidator(0),
        ]
    )

class Mission(UpdatedTimeStamp, LaunchTimeStamp):

    class Status(models.TextChoices):
        PLANNED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'

    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )

    status = models.CharField(
        max_length=9,
        default=Status.PLANNED,
        choices=Status.choices,
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    spacecraft = models.ForeignKey(
        to=Spacecraft,
        on_delete=models.CASCADE,
    )
    astronauts = models.ManyToManyField(
        to=Astronaut,
    )

    commander = models.ForeignKey(
        to=Astronaut,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commander',
    )

    @property
    def comm_name(self):
        return self.commander.name if self.commander else "TBA"

    @property
    def astr_names(self):
        return ", ".join(astr.name for astr in self.astronauts.all())

    def spacewalks(self):
        return sum(astr.spacewalks for astr in self.astronauts.all())
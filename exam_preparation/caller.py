import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from main_app.models import Astronaut, Mission, Spacecraft
from django.db.models import Q, Count, Model, Avg, F


# Import your models here

# Create queries within functions
def get_astronauts(search_string=None) -> str:
    if search_string is None or search_string == "":
        return ""

    astronauts = Astronaut.objects.filter(Q(name__icontains=search_string)
                                          |
                                          Q(phone_number__icontains=search_string)).order_by('name')
    if not astronauts:
        return ""

    return "\n".join(f"Astronaut: {ast.name}, phone number: {ast.phone_number}, status: {ast.status}"
                     for ast in astronauts)


def get_top_astronaut() -> str:

    top_astr = (Astronaut.objects.prefetch_related('mission_set').
                annotate(mission_count=Count('mission_set'))).order_by('-mission_count',
                                                                       'phone_number').first()



    if not top_astr or top_astr.mission_count == 0:
        return "No data."

    return f"Top Astronaut: {top_astr.name} with {top_astr.mission_count} missions."


def get_top_commander() -> str:

    top_astr = (Astronaut.objects.prefetch_related('commander').
                annotate(mission_count=Count('commander'))).order_by('-mission_count',
                                                                       'phone_number').first()



    if not top_astr or top_astr.mission_count == 0:
        return "No data."

    return f"Top Commander: {top_astr.name} with {top_astr.mission_count} missions."

def get_last_completed_mission() -> str:
    mission = Mission.objects.filter(status=Mission.Status.COMPLETED).order_by('-updated_at').first()

    if not mission:
        return "No data."

    return (f"The last completed mission is: {mission.name}. "
            f"Commander: {mission.comm_name()}. Astronauts: {mission.astr_names()}."
            f" Spacecraft: {mission.spacecraft.name}. Total spacewalks: {mission.spacewalks()}.")


def get_most_used_spacecraft()-> str:
    spacecraft = (Spacecraft.objects.prefetch_related("mission_set__astronauts")
                  .annotate(mission_count=Count('mission_set', distinct= True),
                           astronaut_count=Count('mission_set__astronauts', distinct= True))
                  .order_by('-mission_count', 'name').first())

    if not spacecraft or spacecraft.mission_count == 0:
        return "No data."

    return (f"The most used spacecraft is: {spacecraft.name}, "
            f"manufactured by {spacecraft.manufacturer},"
            f" used in {spacecraft.mission_count} missions, "
            f"astronauts on missions: {spacecraft.astronaut_count}.")




def decrease_spacecrafts_weight() -> str:
    # Find unique spacecraft in planned missions with weight >= 200
    affected_spacecrafts = Spacecraft.objects.filter(
        mission__status=Mission.Status.PLANNED,
        weight__gte=200.0
    )

    if not affected_spacecrafts:
        return "No changes in weight."

    # Count affected spacecraft before update
    affected_count = affected_spacecrafts.count()

    # Decrease weight by 200 kg
    affected_spacecrafts.update(weight=F('weight') - 200.0)

    # Calculate average weight of all spacecrafts after update
    avg_weight = Spacecraft.objects.aggregate(Avg('weight'))['weight__avg']

    return (f"The weight of {affected_count} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight:.1f}kg")




print(decrease_spacecrafts_weight())






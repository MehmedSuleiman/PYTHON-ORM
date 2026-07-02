import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
# Create and check models
# Run and print your queries
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout
from django.db.models import When, Value, Case, QuerySet


def show_highest_rated_art() -> str:
    art = ArtworkGallery.objects.order_by("-rating", "id").first()
    return f"{art.art_name} is the highest-rated art with a {art.rating} rating!"

def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([first_art, second_art])

def delete_negative_rated_arts() -> None:
    arts = ArtworkGallery.objects.filter(rating__lt=0)
    for art in arts:
        art.delete()

def show_the_most_expensive_laptop() -> str:
    laptop = Laptop.objects.order_by("-price", "-id").first()
    return f"{laptop.brand} is the most expensive laptop available for {laptop.price}$!"

def bulk_create_laptops(args: list[Laptop]) -> None :
    Laptop.objects.bulk_create(args)

def update_to_512_GB_storage() -> None:
    Laptop.objects.filter(brand__in = [Laptop.Brands.ASUS, Laptop.Brands.LENOVO]).update(storage=512)

def update_to_16_GB_memory()  -> None:
    (Laptop.objects.filter(brand__in = [Laptop.Brands.APPLE, Laptop.Brands.DELL,Laptop.Brands.ACER ])
               .update(memory=16))

def delete_inexpensive_laptops() -> None:
    Laptop.objects.filter(price__lt=1200).delete()

def update_operation_systems()  -> None:
    laptops = Laptop.objects.all()
    for laptop in laptops:
        if laptop.brand == Laptop.Brands.APPLE :
            laptop.operation_system = "MacOS"
        if laptop.brand == Laptop.Brands.ASUS :
            laptop.operation_system = "Windows"
        if laptop.brand == Laptop.Brands.LENOVO :
            laptop.operation_system = "Chrome OS"
        if laptop.brand == Laptop.Brands.DELL or laptop.brand == Laptop.Brands.ACER :
            laptop.operation_system = "Linux"


def bulk_create_chess_players(args: list[ChessPlayer]) -> None:
    ChessPlayer.objects.bulk_create(args)

def delete_chess_players()-> None:
    ChessPlayer.objects.filter(title= "no title").delete()

def change_chess_games_won() -> None:
    ChessPlayer.objects.filter(title ='GM' ).update(games_won = 30)

def change_chess_games_lost()-> None:
    ChessPlayer.objects.filter(title="no title").update(games_won = 25)

def change_chess_games_drawn() -> None:
    ChessPlayer.objects.all().update(games_drawn = 10)

def grand_chess_title_IM():
    ChessPlayer.objects.filter(rating__range= [2399, 2300 ]).update(title ="IM")

def grand_chess_title_FM():
    ChessPlayer.objects.filter(rating__range= [2299, 2200 ]).update(title ="IM")

def grand_chess_title_regular_player() -> None:
    ChessPlayer.objects.filter(rating__range=[2199, 0]).update(title="regular player")

def set_new_chefs() -> None:
    meals = Meal.objects.all()
    updated_meals = []

    for m in meals:
        if m.meal_type == "Breakfast":
            m.chef = "Gordon Ramsay"
            updated_meals.append(m)

        if m.meal_type == "Lunch":
            m.chef = "Julia Child"
            updated_meals.append(m)

        if m.meal_type == "Dinner":
            m.chef = "Jamie Oliver"
            updated_meals.append(m)

        if m.meal_type == "Snack":
            m.chef = "Thomas Keller"
            updated_meals.append(m)

    Meal.objects.bulk_update(updated_meals, ["chef"])

def set_new_preparation_times() -> None:
    meals = Meal.objects.all()
    updated_meals = []

    for m in meals:
        if m.meal_type == "Breakfast":
            m.preparation_time = 10
            updated_meals.append(m)

        if m.meal_type == "Lunch":
            m.preparation_time = 12
            updated_meals.append(m)

        if m.meal_type == "Dinner":
            m.preparation_time = 15
            updated_meals.append(m)

        if m.meal_type == "Snack":
            m.preparation_time = 5
            updated_meals.append(m)

    Meal.objects.bulk_update(updated_meals, ["preparation_time"])

def update_low_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in = [ "Breakfast", "Dinner"]).update(calories = 400)

def update_high_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=["Lunch", "Snack"]).update(calories=700)

def delete_lunch_and_snack_meals()-> None:
    Meal.objects.filter(meal_type__in=["Lunch", "Snack"]).delete()

def show_hard_dungeons() -> str:
    h_dungeons = Dungeon.objects.filter(difficulty= "Hard").order_by("-location")
    return "\n".join(f"{d.name} is guarded by {d.boss_name} who has {d.boss_health} health points!"
                     for d in h_dungeons)

def bulk_create_dungeons(args: list[Dungeon]) -> None:
    Dungeon.objects.bulk_create(args)

def update_dungeon_names()-> None:
    Dungeon.objects.update(
        name = Case(
            When(difficulty = "Easy", then= Value("The Erased Thombs")),
            When(difficulty = "Medium", then= Value("The Coral Labyrinth")),
            When(difficulty = "Hard", then= Value("The Lost Haunt")),
        )
    )

def update_dungeon_bosses_health() -> None:
    Dungeon.objects.exclude(difficulty= "Easy").update(health = 500)

def update_dungeon_recommended_levels() -> None:
    Dungeon.objects.update(
        recomended_level=Case(
            When(difficulty="Easy", then=Value(25)),
            When(difficulty="Medium", then=Value(50)),
            When(difficulty="Hard", then=Value(75)),
        )
    )

def update_dungeon_rewards() -> None :
    Dungeon.objects.update(
        reward=Case(
            When(boss_health=500, then=Value("1000 Gold")),
            When(location__startswith= "E", then=Value("New dungeon unlocked")),
            When(location__endswith="s", then=Value("Dragonheart Amulet")),
        )
    )

def set_new_locations() -> None:
    Dungeon.objects.update(
        location = Case(
            When(recommended_level=25, then=Value("Enchanted Maze")),
            When(recommended_level=50, then=Value("Grimstone Mines")),
            When(recommended_level=75, then=Value("Shadowed Abyss")),
        )
    )

def show_workouts() -> str:
    workouts = Workout.objects.filter(
        workout_type__in=[
            "Calisthenics",
            "CrossFit",
        ]
    ).order_by('id')

    return '\n'.join(f"{w.name} from {w.workout_type} type has {w.difficulty} difficulty!" for w in workouts)

def get_high_difficulty_cardio_workouts() -> QuerySet[Workout]:
    return Workout.objects.filter(
        difficulty="High",
        workout_type="Cardio",
    ).order_by('instructor')


def set_new_instructors() -> None:
    Workout.objects.update(
        instructor=Case(
            When(workout_type="Cardio", then=Value("John Smith")),
            When(workout_type="Strength", then=Value("Michael Williams")),
            When(workout_type="Yoga", then=Value("Emily Johnson")),
            When(workout_type="CrossFit", then=Value("Sarah Davis")),
            When(workout_type="Calisthenics", then=Value("Chris Heria")),
        )
    )
def set_new_duration_times() -> None:
    Workout.objects.update(
        duration=Case(
            When(instructor="John Smith", then=Value("15 minutes")),
            When(instructor="Sarah Davis", then=Value("30 minutes")),
            When(instructor="Chris Heria", then=Value("45 minutes")),
            When(instructor="Michael Williams", then=Value("1 hour")),
            When(instructor="Emily Johnson", then=Value("1 hour and 30 minutes")),
        )
    )

def delete_workouts() -> None:
    Workout.objects.exclude(workout_type__in=["Strength", "Calisthenics"]).delete()
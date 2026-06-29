import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
# Create and check models
# Run and print your queries
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal


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


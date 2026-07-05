import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Author, Book, Song, Artist, Product, Review, DrivingLicense, Driver, Owner, Registration, \
    Car

from datetime import date, timedelta, datetime
from django.db.models import QuerySet, Model


# Create queries within functions


def show_all_authors_with_their_books() -> str:
    authors = Author.objects.all()
    result = []
    for author in authors:
        books = author.books.all()
        result.append(f"{author.name} has written - {', '.join(str(b) for b in books)}!" )
    return "\n".join(result)

def delete_all_authors_without_books() -> None:
    authors = Author.objects.all()
    for author in authors:
        if author.books.count() == 0:
            author.delete()


def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)

def get_songs_by_artist(artist_name: str) -> QuerySet:
    artist = Artist.objects.get(name=artist_name)
    songs = artist.songs.all().order_by("-id")
    return songs

def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title = song_title)
    artist.songs.remove(song)

def calculate_average_rating_for_product_by_name(product_name: str) -> float:
    product = Product.objects.get(name=product_name)
    rating = sum(review.rating for review in product.reviews.all()) / product.reviews.count()
    return rating

def get_reviews_with_high_ratings(threshold: int) -> QuerySet[Review]:
    return Review.objects.filter(review_rating__gte=threshold)

def get_products_with_no_reviews() :
    products = Product.objects.all().order_by("-name")
    p_with_no_reviews = []

    for product in products:
        if product.reviews.count() == 0:
            p_with_no_reviews.append(product)

    return p_with_no_reviews

def delete_products_without_reviews() -> None:
    products = Product.objects.all()

    for product in products:
        if product.reviews.count() == 0:
            product.delete()



def calculate_licenses_expiration_dates()-> str:
    licenses = DrivingLicense.objects.order_by("-license_number")
    return "\n".join(str(l) for l in licenses)

def get_drivers_with_expired_licenses(due_date: date) -> QuerySet[Driver]:
    return Driver.objects.filter(
        license__issue_date__lt=due_date - timedelta(days=365),
    )

def register_car_by_owner(owner: Owner) -> str:
    registration = Registration.objects.filter(car__isnull= True).first()
    car = Car.objects.filter(registration__isnull= True).first()

    registration.car = car
    registration.registration_date = datetime.today()
    registration.save()

    car.owner = owner
    car.save()
    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."

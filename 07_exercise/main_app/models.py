from django.core.validators import MinValueValidator, RegexValidator,  MinLengthValidator
from django.db import models
from psycopg2._psycopg import Decimal

from main_app.mixins import RechargeEnergyMixin
from main_app.validators import name_validator


# Create your models here.
class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[name_validator]
        )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(
            limit_value=18,
            message="Age must be greater than or equal to 18"
        )
        ]
    )
    email = models.EmailField(
        error_messages={"invalid": "Enter a valid email address"},
    )
    phone_number = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex= r"^\+359\d{9}$",
                message="Phone number must start with '+359' followed by 9 digits"
            )
        ]
    )

    website_url = models.URLField(
        error_messages={'invalid': "Enter a valid URL"}
    )


class BaseMedia(models.Model):
    title = models.CharField(
        max_length=100,
    )
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']

class Movie(BaseMedia):
    director = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                limit_value=8,
                message="Director must be at least 8 characters long"
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"


class Book(BaseMedia):
    author = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                limit_value=5,
                message="Author must be at least 5 characters long"
            )
        ]
    )

    isbn = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                limit_value=6,
                message="ISBN must be at least 6 characters long"
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"


class Music(BaseMedia):
    ARTIST_MAX_LENGTH: int = 100
    ARTIST_MIN_LENGTH: int = 9

    artist = models.CharField(
        max_length=ARTIST_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                limit_value=ARTIST_MIN_LENGTH,
                message=f"Artist must be at least {ARTIST_MIN_LENGTH} characters long"
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"


class Product(models.Model):
    TAX : Decimal = Decimal("0,08")
    WEIGHT_COST : Decimal = Decimal("2")
    STR : str = "Product"

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_tax(self) -> Decimal:
        return self.price * self.TAX

    def calculate_shipping_cost(self, weight: Decimal) -> Decimal:
        return weight * self.WEIGHT_COST

    def format_product_name(self) -> str:
        return f"{self.STR}: {self.name}"


class DiscountedProduct(Product):
    PRICE_WITHOUT_DISCOUNT : Decimal = Decimal("0,2")
    TAX: Decimal = Decimal("0,05")
    WEIGHT_COST: Decimal = Decimal("1,5")
    STR : str = "Discounted Product"

    def calculate_price_without_discount(self) -> Decimal:
        return self.price + (self.price * self.PRICE_WITHOUT_DISCOUNT)

    class Meta:
        proxy = True


class Hero(models.Model, RechargeEnergyMixin):
    REQUIRED_ENERGY: int = 0

    name = models.CharField(
        max_length=100,
    )
    hero_title = models.CharField(
        max_length=100,
    )
    energy = models.PositiveIntegerField()

    @property
    def not_enough_energy_message(self) -> str:
        raise NotImplemented

    @property
    def successful_ability_usage_message(self) -> str:
        raise NotImplemented

    def use_ability(self) -> str:
        if self.energy < self.REQUIRED_ENERGY:
            return self.not_enough_energy_message

        self.energy = max(self.energy - self.REQUIRED_ENERGY, 1)

        return self.successful_ability_usage_message


class FlashHero(Hero):
    REQUIRED_ENERGY: int = 65

    @property
    def not_enough_energy_message(self) -> str:
        return f"{self.name} as Flash Hero needs to recharge the speed force"

    @property
    def successful_ability_usage_message(self) -> str:
        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    def run_at_super_speed(self) -> str:
        return self.use_ability()

    class Meta:
        proxy = True


class SpiderHero(Hero):
    REQUIRED_ENERGY: int = 80

    @property
    def not_enough_energy_message(self) -> str:
        return f"{self.name} as Spider Hero is out of web shooter fluid"

    @property
    def successful_ability_usage_message(self) -> str:
        return f"{self.name} as Spider Hero swings from buildings using web shooters"

    def swing_from_buildings(self) -> str:
        return self.use_ability()

    class Meta:
        proxy = True
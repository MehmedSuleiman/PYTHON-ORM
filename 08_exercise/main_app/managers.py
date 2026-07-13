from decimal import Decimal

from django.db import models
from django.db.models import QuerySet, Q, Count



class RealEstateListingManager(models.Manager):

    def by_property_type(self, property_type: str) -> QuerySet:
        property_type_queryset = self.filter(property_type=property_type)
        return property_type_queryset

    def in_price_range(self, min_price: Decimal, max_price: Decimal) -> QuerySet:

        property_queryset = self.filter(Q(price__gte=min_price) & Q(price__lte=max_price))
        return property_queryset

    def with_bedrooms(self, bedrooms_count: int) -> QuerySet:
        props = self.filter(bedrooms=bedrooms_count)
        return props

    def popular_locations(self) -> QuerySet:
        popular_locations = (self.values('location').annotate(location_count=Count('location'))
                             .order_by('-location_count', 'location'))

        return popular_locations[:2]
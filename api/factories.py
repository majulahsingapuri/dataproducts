import factory
from django.contrib.gis.geos import Point
from faker.providers import BaseProvider

from .models import Location


class DjangoGeoPointProvider(BaseProvider):
    def geo_point(self, **kwargs):
        faker = factory.faker.faker.Faker()
        coords = faker.latlng(**kwargs)
        return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)


class LocationFactory(factory.django.DjangoModelFactory):
    factory.Faker.add_provider(DjangoGeoPointProvider)

    class Meta:
        model = Location

    name = factory.Sequence(lambda n: f"Location {n}")
    coordinate = factory.Faker("geo_point")

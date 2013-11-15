from django.contrib.auth.models import User
from django.test import TestCase

from .models import Account, Station
from .weather import get_current_weather


# Create your tests here.
class GetWeatherTests(TestCase):
    def test_get_current_conditions(self):
        result = get_current_weather()

        self.assertIsNotNone(result["response"]["current_observation"])


class StationTests(TestCase):

    def setUp(self):
        user = User.objects.create_user("test", "test@test.com")
        self.account = Account.objects.create(ip="192.168.2.6", port="8080", user=user)
        for i in range(1, 9):
            Station.objects.create(account=self.account, number=i)

    def test_stations(self):
        for station in Station.objects.all():
            station.enable(60)
        for station in Station.objects.all():
            self.assertTrue(station.status)
            station.disable()
        for station in Station.objects.all():
            self.assertFalse(station.status)



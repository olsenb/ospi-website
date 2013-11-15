from django.contrib.auth.models import User
from django.test import TestCase

from .weather import get_current_weather, get_forecast_weather
from .models import Account, Station


# Create your tests here.
class GetWeatherTests(TestCase):
    def test_get_current_weather(self):
        result = get_current_weather()

        self.assertIsNotNone(result["current_observation"])

        root = result["current_observation"]

        self.assertGreaterEqual(root["temp_f"], 0)
        self.assertIsNotNone(root["precip_1hr_in"])
        self.assertIsNotNone(root["relative_humidity"])

    def test_get_forecast_weather(self):
        result = get_forecast_weather()

        self.assertIsNotNone(result["forecast"])

        for forecast in result["forecast"]["simpleforecast"]["forecastday"]:
            self.assertIsNotNone(forecast["high"]["fahrenheit"])
            self.assertIsNotNone(forecast["low"]["fahrenheit"])
            self.assertIsNotNone(forecast["qpf_allday"]["in"])
            self.assertIsNotNone(forecast["minhumidity"])


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


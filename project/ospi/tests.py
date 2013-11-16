from django.contrib.auth.models import User
from django.test import TestCase
from datetime import datetime
from .weather import get_current_weather, get_forecast_weather, get_geo_lookup
from .models import Account, Station, ForecastWeatherManager


# Create your tests here.
class WeatherTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('myuser', 'myemail@test.com', 'mypassword')
        self.account = Account.objects.create(user=self.user, ip="127.0.0.0", weather_api="some_api_key",
                                              zip_code="84770")

    def test_get_current_weather(self):
        result = get_current_weather(self.account)

        self.assertIsNotNone(result["current_observation"])

        root = result["current_observation"]

        self.assertGreaterEqual(root["temp_f"], 0)
        self.assertIsNotNone(root["precip_1hr_in"])
        self.assertIsNotNone(root["relative_humidity"])

    def test_get_forecast_weather(self):
        result = get_forecast_weather(self.account)

        self.assertIsNotNone(result["forecast"])

        for forecast in result["forecast"]["simpleforecast"]["forecastday"]:
            self.assertIsNotNone(forecast["high"]["fahrenheit"])
            self.assertIsNotNone(forecast["low"]["fahrenheit"])
            self.assertIsNotNone(forecast["qpf_allday"]["in"])
            self.assertIsNotNone(forecast["minhumidity"])

    def test_get_geo_lookup(self):
        result = get_geo_lookup(self.account)

        self.assertIsNotNone(result["location"])
        self.assertEquals("84770", result["location"]["zip"])
        self.assertEquals("Saint George", result["location"]["city"])
        self.assertEquals("UT", result["location"]["state"])


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


class ForecastWeatherManagerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('myuser', 'myemail@test.com', 'mypassword')
        self.account = Account.objects.create(user=self.user, ip="127.0.0.0", weather_api="some_api_key",
                                              zip_code="84770")

    def test_fetch(self):
        forecasts = ForecastWeatherManager.fetch(self.account)

        self.assertEquals(len(forecasts), 4)
        self.assertEquals(forecasts[0].day, datetime(2013, 11, 15))
        self.assertEquals(forecasts[0].high, "70")
        self.assertEquals(forecasts[0].low, "34")
        self.assertEquals(forecasts[0].rain, 0.0)
        self.assertEquals(forecasts[0].humidity, 24)


class CronTests(TestCase):

    def test_pull_data(self):
        pass
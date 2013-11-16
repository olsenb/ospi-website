from django.contrib.auth.models import User
from django.test import TestCase
import datetime
from .weather import get_current_weather, get_forecast_weather, get_geo_lookup
from .models import Account, ForecastWeatherManager, ForecastWeather, Schedule, Station
from .cron import pull_data
from django.utils import timezone

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
        self.account = Account.objects.create(ip="192.168.2.6", port="8080", user=user, weather_api="some_api_key",
                                              zip_code="84770")
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

    def test_binary_clock(self):
        time = timezone.now()
        end_time = time + datetime.timedelta(seconds=60)
        stations = Station.objects.all().order_by('number')
        while timezone.now() < end_time:
            seconds = timezone.now().time().second
            if 32 <= seconds:
                stations[0].enable()
                seconds -= 32
            else:
                stations[0].disable()
            if 16 <= seconds:
                stations[1].enable()
                seconds -= 16
            else:
                stations[1].disable()
            if 8 <= seconds:
                stations[2].enable()
                seconds -= 8
            else:
                stations[2].disable()
            if 4 <= seconds:
                stations[3].enable()
                seconds -= 4
            else:
                stations[3].disable()
            if 2 <= 2:
                stations[4].enable()
                seconds -= 2
            else:
                stations[4].disable()
            if 1 <= seconds:
                stations[5].enable()
            else:
                stations[5].disable()
        for x in range(0,6):
            stations[x].disable()


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

    def setUp(self):
        self.user = User.objects.create_superuser('myuser', 'myemail@test.com', 'mypassword')
        self.account = Account.objects.create(user=self.user, ip="127.0.0.0", weather_api="some_api_key",
                                              zip_code="84770")

    def test_pull_data(self):
        self.assertEquals(len(ForecastWeather.objects.all()), 0)

        self.account.city = "Flagstaff"
        self.account.state = "AZ"
        self.account.save()

        pull_data()

        self.assertNotEqual(self.account.city, "Saint_George")
        self.assertNotEqual(self.account.state, "UT")
        self.assertEquals(len(ForecastWeather.objects.all()), 4)

    def test_pull_data_no_city_or_state(self):
        self.assertEquals(len(ForecastWeather.objects.all()), 0)

        pull_data()

        self.account = Account.objects.get(id=self.account.id)
        self.assertEquals(self.account.city, "Saint_George")
        self.assertEquals(self.account.state, "UT")
        self.assertEquals(len(ForecastWeather.objects.all()), 4)


class ScheduleTests(TestCase):

    def setUp(self):
        pass

    def test_check_schedule_raining_today(self):
        schedule = Schedule.objects.create()

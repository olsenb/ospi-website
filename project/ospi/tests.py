from django.test import TestCase
from .weather import get_current_weather, get_forecast_weather

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

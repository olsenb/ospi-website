from django.test import TestCase
from .weather import get_current_weather

# Create your tests here.
class GetWeatherTests(TestCase):
    def test_get_current_conditions(self):
        result = get_current_weather()

        self.assertIsNotNone(result["response"]["current_observation"])

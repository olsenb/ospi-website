from django.conf import settings
import requests
import json
import os

WUNDER_GROUND_URL = 'http://api.wunderground.com/api/fa092a1bdf600850/%s/q/UT/Saint_George.json'


def get_current_weather():
    if settings.USE_TEST_DATA:
        return json.load(open(os.path.join(os.path.dirname(__file__), "templates/Current_Saint_George.json")))
    method = 'conditions'
    return get_results(method)


def get_forecast_weather():
    if settings.USE_TEST_DATA:
        return json.load(open(os.path.join(os.path.dirname(__file__), "templates/Forecast_Saint_George.json")))
    method = 'forecast'
    return get_results(method)


def get_results(method):
    url = WUNDER_GROUND_URL % method
    r = requests.get(url)
    return json.load(r.text)
from django.conf import settings
import requests
import json
import os

WUNDER_GROUND_URL = 'http://api.wunderground.com/api/%s/%s/q/UT/Saint_George.json'


def get_current_weather(api_key):
    if settings.USE_TEST_DATA:
        return json.load(open(os.path.join(os.path.dirname(__file__), "templates/Current_Saint_George.json")))
    return get_results(api_key, 'conditions')


def get_forecast_weather(api_key):
    if settings.USE_TEST_DATA:
        return json.load(open(os.path.join(os.path.dirname(__file__), "templates/Forecast_Saint_George.json")))
    return get_results(api_key, 'forecast')


def get_geo_lookup(api_key):
    if settings.USE_TEST_DATA:
        return json.load(open(os.path.join(os.path.dirname(__file__), "templates/Geo_Lookup_Saint_George.json")))
    return get_results(api_key, 'geolookup')


def get_results(api_key, method):
    url = WUNDER_GROUND_URL % (api_key, method)
    r = requests.get(url)
    return json.load(r.text)
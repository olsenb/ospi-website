from django.conf import settings
import requests
import json
import os

WUNDER_GROUND_URL = 'http://api.wunderground.com/api/%s/%s/q/%s.json'


def get_current_weather(account):
    if settings.USE_TEST_DATA:
        return json.load(open(os.path.join(os.path.dirname(__file__), "templates/Current_Saint_George.json")))
    return base_helper_function(account.weather_api, 'conditions', account.state, account.city)


def get_forecast_weather(account):
    if settings.USE_TEST_DATA:
        return json.load(open(os.path.join(os.path.dirname(__file__), "templates/Forecast_Saint_George.json")))
    return base_helper_function(account.weather_api, 'forecast', account.state, account.city)


def get_geo_lookup(account):
    if settings.USE_TEST_DATA:
        return json.load(open(os.path.join(os.path.dirname(__file__), "templates/Geo_Lookup_Saint_George.json")))
    return get_results(account.weather_api, 'geolookup', account.zip_code)


def base_helper_function(api_key, method, state, city):
    return get_results(api_key, method, "%s/%s".format(state, city))


def get_results(api_key, method, lookup_key):
    url = WUNDER_GROUND_URL % (api_key, method, lookup_key)
    r = requests.get(url)
    return json.load(r.text)
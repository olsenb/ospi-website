import requests
import json

WUNDER_GROUND_URL = 'http://api.wunderground.com/api/%s/%s/q/%s.json'


def get_current_weather(account):
    return base_helper_function(account.weather_api, 'conditions', "UT", "Saint_George")


def get_forecast_weather(account):
    return base_helper_function(account.weather_api, 'forecast', "UT", "Saint_George")


def get_geo_lookup(account):
    return get_results(account.weather_api, 'geolookup', "84790")


def base_helper_function(api_key, method, state, city):
    return get_results(api_key, method, "%s/%s" % (state, city))


def get_results(api_key, method, lookup_key):
    url = WUNDER_GROUND_URL % (api_key, method, lookup_key)
    r = requests.get(url)
    return json.loads(r.text)
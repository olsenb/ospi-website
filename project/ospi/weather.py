import requests
import json

WUNDER_GROUND_URL = 'http://api.wunderground.com/api/fa092a1bdf600850/%s/q/UT/Saint_George.json'

def get_current_weather():
    method = 'conditions'
    url = WUNDER_GROUND_URL % method
    r = requests.get(url)
    return json.loads(r.text)
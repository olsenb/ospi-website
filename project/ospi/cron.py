from .views import *
from django.utils import timezone
from weather import get_geo_lookup
import kronos


@kronos.register('* * * * *')
def update_log():
    accounts = Account.objects.all()
    for account in accounts:
        status = account.get_status()
        for idx, station in enumerate(status['stations']):
            try:
                mystation = Station.objects.get(number=idx+1, account=account)
            except Station.DoesNotExist:
                continue
            try:
                running = WaterLog.objects.get(end_time__isnull=True, account=account, station=mystation)
            except WaterLog.DoesNotExist:
                running = False
            except WaterLog.MultipleObjectsReturned:
                raise

            if station and not running:
                #Create Log
                WaterLog.objects.create(account=account, station=mystation, start_time=timezone.now())
            elif station is False and running:
                #End log
                running.end_time = timezone.now()
                running.save()


@kronos.register('0 */4 * * *')
def pull_data():
    accounts = Account.objects.all()
    for account in accounts:
        if not account.zip:
            data = get_geo_lookup(account)
            account.city = data["location"]["city"]
            account.state = data["location"]["state"]
            account.save()
        forecasts = ForecastWeather.objects.fetch(account)
        for forecast in forecasts:
            forecast.save()

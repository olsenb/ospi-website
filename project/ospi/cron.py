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


@kronos.register('0 1 * * *')
def pull_data():
    six_am = datetime.time(6)
    eight_am = datetime.time(8)
    half_hour = datetime.time(0, 30)
    five_minutes = datetime.time(0, 5)

    accounts = Account.objects.all()
    for account in accounts:
        if account.zip_code and not account.city or not account.state:
            data = get_geo_lookup(account)
            temp_city = data["location"]["city"].replace('-', '_')
            temp_city = temp_city.replace(' ', '_')
            account.city = temp_city
            account.state = data["location"]["state"]
            account.save()
        forecasts = ForecastWeather.objects.fetch(account)
        for forecast in forecasts:
            forecast.save()
        try:
            schedule = Schedule.objects.filter(account=account)[0]
        except IndexError:
            schedule = Schedule.objects.create(account=account, name="Primary", start_time=six_am, end_time=eight_am,
                                               repeat=half_hour, run_time=five_minutes)
        schedule.check_schedule(forecasts)
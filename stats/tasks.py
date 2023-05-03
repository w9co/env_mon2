from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail
import requests
from sense_hat import SenseHat



def make_stats():
    sense = SenseHat()
    ptemp = sense.get_temperature_from_pressure()
    htemp = sense.get_temperature_from_humidity()
    avg_temp = (ptemp + htemp) / 2 # average vals from both sensors
    temperature = convert_to_f(avg_temp)
    temp_adjustment = -7.88
    temperature = temperature + temp_adjustment # adjust temperature
    humidity = sense.humidity
    pressure = sense.pressure * 0.0295300 # convert to Mg
    outside_temp = get_outside_temp()

    # weather api call frequently fails.  Use last temp to
    # avoid completely wrecking averages with a 0, while maintaining
    # the dataset graph.js expects
    if outside_temp == 0:
        outside_temp = get_prev_outside_temp();

    Stats = apps.get_model('stats.Stats')
    Stats.objects.create(
        temperature = temperature,
        humidity = humidity,
        pressure = pressure,
        outside_temp = outside_temp,
    )

def get_prev_outside_temp():
    Stats = apps.get_model('stats.Stats')
    stat = Stats.objects.latest('id');
    return stat.outside_temp

def get_outside_temp():
    try:
        url = 'https://api.weather.gov/stations/KTYQ/observations/latest'
        response = requests.get(url, timeout=1)
        res_obj = response.json()
        temp = res_obj['properties']['temperature']['value']
        return convert_to_f(temp)
    except:
        return 0


def convert_to_f(temp_in_c):
    return temp_in_c * 1.8 + 32


def send_alerts():
    high_temp_threshold = 75
    low_temp_threshold = 69
    Stats = apps.get_model('stats.Stats')
    stat = Stats.objects.latest('id');
    temp = stat.temperature
    message = 'The temperature in the office is currently {}.'.format(temp)

    if temp > high_temp_threshold or temp < low_temp_threshold:
        alert_list = settings.TEMP_ALERT_RECIPIENTS
        send_mail(
            'Temperature Alert',
            message,
            'noreply@ivytech.edu',
            alert_list,
        )


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(make_stats, 'interval', minutes=10)
    scheduler.add_job(send_alerts, 'cron', day_of_week='mon-fri', hour=6) 
    scheduler.start()

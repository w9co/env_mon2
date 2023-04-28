from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import apps
import requests
from sense_hat import SenseHat



def make_stats():
    sense = SenseHat()
    ptemp = sense.get_temperature_from_pressure()
    htemp = sense.get_temperature_from_humidity()
    avg_temp = (ptemp + htemp) / 2 # average vals from both sensors
    temperature = convert_to_f(avg_temp)
    temp_adjustment = -20
    temperature = temperature + temp_adjustment # adjust temperature
    humidity = sense.humidity
    pressure = sense.pressure * 0.0295300 # convert to Mg
    outside_temp = get_outside_temp()

    Stats = apps.get_model('stats.Stats')
    Stats.objects.create(
        temperature = temperature,
        humidity = humidity,
        pressure = pressure,
        outside_temp = outside_temp,
    )


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


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(make_stats, 'interval', minutes=10)
    scheduler.start()

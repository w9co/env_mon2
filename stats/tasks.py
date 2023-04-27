from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import apps
from sense_hat import SenseHat



def make_stats():
    sense = SenseHat()
    ptemp = sense.get_temperature_from_pressure()
    htemp = sense.get_temperature_from_humidity()
    avg_temp = (ptemp + htemp) / 2 # average vals from both sensors
    temperature = avg_temp * 1.8 + 32 # convert to F
    temp_adjustment = -20
    temperature = temperature + temp_adjustment # adjust temperature
    humidity = sense.humidity
    pressure = sense.pressure * 0.0295300 # convert to Mg

    Stats = apps.get_model('stats.Stats')
    Stats.objects.create(
        temperature = temperature,
        humidity = humidity,
        pressure = pressure
    )


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(make_stats, 'interval', minutes=10)
    scheduler.start()

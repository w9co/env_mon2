from django.db import models
from django.utils import timezone



class Stats(models.Model):
    created = models.DateTimeField(default=timezone.now)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    pressure = models.DecimalField(max_digits=5, decimal_places=2)
    outside_temp = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return '{} -- Temp: {}, Humidity: {}, Pressure: {}'.format(
            self.created,
            self.temperature,
            self.humidity,
            self.pressure,
        )    



from datetime import datetime, timedelta
import pytz

from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import FormView

from . import forms, models



class Index(FormView):
    template_name = 'stats/index.html'
    form_class = forms.statsSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.now()
        day_ago = now - timedelta(days=1)

        try:
            start_date = self.request.GET.get('start_date')
            if start_date:
                start_date = datetime.strptime(start_date, '%m/%d/%Y %I:%M %p')
            else:
                start_date = day_ago
        except Exception as e:
            messages.warning(self.request, 'Invalid start date selected')
            start_date = day_ago

        try:
            end_date = self.request.GET.get('end_date')
            if end_date:
                end_date = datetime.strptime(end_date, '%m/%d/%Y %I:%M %p')
            else:
                end_date = now
        except Exception as e:
            messages.warning(self.request, 'Invalid end date selected')
            end_date = now

        start_date = start_date.astimezone(pytz.UTC)
        end_date = end_date.astimezone(pytz.UTC)

        stats = models.Stats.objects.filter(
            created__gte=start_date,
            created__lte=end_date,
        ).values_list(
            'created',
            'temperature',
            'humidity',
            'pressure',
            'outside_temp',
            named=True
        ).order_by('created')
        dates = [stat.created.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d %I:%M %p') for stat in stats]
        temps = [stat.temperature.to_eng_string() for stat in stats]
        hums = [stat.humidity.to_eng_string() for stat in stats]
        press = [stat.pressure.to_eng_string() for stat in stats]
        ext_temps = [stat.outside_temp.to_eng_string() for stat in stats]

        current = models.Stats.objects.latest('created')

        context.update({
            'full_stats': stats,
            'curr_temp': current.temperature,
            'curr_humidity': current.humidity,
            'curr_pressure': current.pressure,
            'curr_outside_temp': current.outside_temp,
            'labels': dates,
            'temp_chart_data': temps,
            'humidity_chart_data': hums,
            'pressure_chart_data': press,
            'outside_temp_chart_data': ext_temps,
        })

        return context

from django.views import generic
from dash.models import Rating
from website.forms import *


class DoctorProfileView(generic.DetailView):
    model = Doctor
    template_name = 'website/doctor_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['ratings'] = context['object'].appointment_set.filter(rating__isnull=False,
                                                                      rating__status=Rating.APPROVED).order_by(
            'datetime')[:10]

        startdt = datetime.datetime.today()
        start_month = (startdt.month + 2) % 12 + 1
        start_year = startdt.year

        if start_month < startdt.month:
            start_year += 1

        enddt = datetime.datetime(start_year, start_month, startdt.day, startdt.hour, startdt.minute, 0, 0)
        context['free_schedule'] = context['object'].get_free_schedule(startdt, enddt)

        return context

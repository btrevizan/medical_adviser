from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from dash.models import Appointment
from django.shortcuts import render
from django.views import generic
from website.forms import *


class AppointmentCreateView(generic.CreateView):
    model = Appointment
    template_name = 'website/create_appointment_error.html'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = AppointmentForm(request.POST)

        if form.is_valid():
            user = request.user
            appointment = Appointment(doctor_id=form.cleaned_data['doctor'],
                                      patient_id=user.id,
                                      datetime=form.cleaned_data['datetime'])
            appointment.save()

            return HttpResponseRedirect('success')
        else:
            return render(request, self.template_name, {'form': form})


class AppointmentCreateSuccessView(generic.TemplateView):
    template_name = 'website/create_appointment_success.html'

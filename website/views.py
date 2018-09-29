from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from .models import *
from .forms import *


class IndexView(generic.TemplateView):
    template_name = 'medical_advisor/index.html' 


class AppointmentCreateView(generic.CreateView):
    model = Appointment
    template_name = 'medical_advisor/create_appointment.html'

    #@method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = Appointment(doctor=form.doctor, patient=form.patient, datetime=form.datetime)
            appointment.save()

            HttpResponseRedirect('appointment/create/success')
        else:
            render(request, self.template_name, {'form': form})


class AppointmentCreateSuccessView(generic.TemplateView):
    template_name = 'website/create_appointment_success.html'

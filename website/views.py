from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from .models import *
from .forms import *


class IndexView(generic.TemplateView):
    template_name = 'website/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'search_form': SearchDoctorForm()})


class AppointmentCreateView(generic.CreateView):
    model = Appointment
    template_name = 'website/create_appointment_error.html'

    # @method_decorator(login_required)
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


class SearchDoctorView(generic.ListView):
    model = Doctor
    template_name = 'website/search_doctor_results.html'
    context_object_name = 'doctors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SearchDoctorForm(self.request.GET)

        if form.is_valid():
            obj_name = self.context_object_name
            context[obj_name] = context[obj_name].filter(speciality__icontains=form.cleaned_data['speciality'],
                                                         address__city__icontains=form.cleaned_data['city'],
                                                         address__neighborhood__icontains=form.cleaned_data['neighborhood'])

            context[obj_name] = [doctor for doctor in context[obj_name]
                                 if doctor.has_free_schedule(form.cleaned_data['startdt'], form.cleaned_data['enddt'])]

            return context
        else:
            HttpResponseRedirect('/')
            
            
class DoctorProfileView(generic.DetailView):
    model = Doctor
    template_name = 'website/doctor_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

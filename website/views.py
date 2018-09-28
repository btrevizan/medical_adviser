from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic
from .models import *
from .forms import *



class IndexView(generic.TemplateView):
    template_name = 'website/index.html'


class AppointmentCreateView(generic.CreateView):
    model = Appointment
    template_name = 'website/create_appointment_error.html'

    @method_decorator(login_required)
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


# ------------------------------------------------------------------------------------------------------------
# No caso de o usuário não preencher algum dos campos (speciality),
#  deverá ser passado no parâmetro a string "NULL".
def SearchDoctor(request, speciality):
    all_doctors = Doctor.objects.all()
    result = list(all_doctors)

    if speciality != "NULL":
        for d in all_doctors:
            if d.speciality != speciality:
                result.remove(d)

    template = loader.get_template('website/templateTestePesquisarMedico.html')   # Template teste.
    context = { 
        'doctors_list': result,
    }
    return HttpResponse(template.render(context, request))


# ------------------------------------------------------------------------------------------------------------

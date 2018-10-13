from django.views.generic import TemplateView, DetailView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from dash.models import Appointment, Patient
from django.urls import reverse_lazy
from datetime import datetime


class AppointmentListView(PermissionRequiredMixin, TemplateView):
    model = Appointment
    context_object_name = 'appointments'
    template_name = 'dash/appointments.html'
    permission_required = 'dash.view_appointment'

    def get_context_data(self, **kwargs):
        patient = self.request.user.patient
        appointments = self.model.objects.filter(patient_id=patient.id)

        open_appointments = appointments.filter(datetime__gte=datetime.today()).order_by('datetime')
        closed_appointments = appointments.filter(datetime__lt=datetime.today()).order_by('-datetime')

        context = {'open_appointments': open_appointments, 'closed_appointments': closed_appointments}
        return context


class AppointmentDetailView(PermissionRequiredMixin, DetailView):
    model = Appointment
    context_object_name = 'appointment'
    template_name = 'dash/appointment_detail.html'
    permission_required = 'dash.view_appointment'


class AppointmentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Patient
    form_class = Patient
    template_name = 'dash/rating_delete.html'
    context_object_name = 'bank_account'
    success_url = reverse_lazy('bank-account-list')

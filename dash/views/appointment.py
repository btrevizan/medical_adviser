from django.views.generic import TemplateView, DetailView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from dash.models import Appointment, Patient
from django.urls import reverse_lazy
from datetime import datetime, timedelta


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
    model = Appointment
    template_name = 'dash/appointment_delete.html'
    context_object_name = 'appointment'
    success_url = reverse_lazy('appointment-list')
    permission_required = 'dash.delete_appointment'

    def can_cancel(self, object):
        return object.datetime >= datetime.today() + timedelta(hours=24)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_cancel'] = self.can_cancel(context[self.context_object_name])
        return context

    def post(self, request, *args, **kwargs):
        appointment = get_object_or_404(self.model, pk=kwargs['pk'])

        if self.can_cancel(appointment):
            return super().post(request, *args, **kwargs)

        return render(request, self.template_name, {'can_cancel': False})
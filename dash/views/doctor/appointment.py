from django.views.generic import TemplateView, DetailView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from dash.decorators import doctor_required
from datetime import datetime, timedelta
from dash.models import Appointment
from django.urls import reverse_lazy

@method_decorator(doctor_required, name='dispatch')
class DoctorAppointmentListView(PermissionRequiredMixin, TemplateView):
    model = Appointment
    context_object_name = 'doctor-appointments'
    template_name = 'dash/appointments.html'
    permission_required = 'dash.view_appointment'

    def get_context_data(self, **kwargs):
        doctor = self.request.user.doctor
        appointments = self.model.objects.filter(doctor_id=doctor.id)

        open_appointments = appointments.filter(datetime__gte=datetime.today()).order_by('datetime')
        closed_appointments = appointments.filter(datetime__lt=datetime.today()).order_by('-datetime')

        context = {'open_appointments': open_appointments, 'closed_appointments': closed_appointments}
        return context

@method_decorator(doctor_required, name='dispatch')
class DoctorAppointmentDetailView(PermissionRequiredMixin, DetailView):
    model = Appointment
    context_object_name = 'appointment'
    template_name = 'dash/doctor_appointment_detail.html'
    permission_required = 'dash.view_appointment'


@method_decorator(doctor_required, name='dispatch')
class DoctorAppointmentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'dash/appointment_delete.html'
    context_object_name = 'appointment'
    success_url = reverse_lazy('doctor-appointment-list')
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
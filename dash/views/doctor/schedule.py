from django.views.generic import TemplateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from dash.decorators import doctor_required
from dash.models import DaySchedule
from dash.models import TimeSchedule
from django.urls import reverse_lazy
import datetime


class Schedule:
    def __init__(self, day):
        self.day = day
        self.times = []


@method_decorator(doctor_required, name='dispatch')
class DoctorSchedule(PermissionRequiredMixin, TemplateView):
    model = DaySchedule
    context_object_name = 'days_times'
    template_name = 'dash/doctor_schedule.html'
    permission_required = "dash.view_dayschedule"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        days_times = []

        doctor = self.request.user.doctor
        days = self.model.objects.filter(doctor_id=doctor.id).order_by('day')

        for d in days:
            daytime = Schedule(d)
            daytime.times = TimeSchedule.objects.filter(day_id=d.id).order_by('start_time')
            days_times.append(daytime)

        context[self.context_object_name] = days_times
        context['all_days'] = list(range(0, 7))

        return context


@method_decorator(doctor_required, name='dispatch')
class DoctorCreateSchedule(PermissionRequiredMixin, TemplateView):
    model = DaySchedule
    context_object_name = 'days_times'
    permission_required = "dash.add_dayschedule"
    success_url = reverse_lazy('doctor-schedule')
    template_name = 'dash/doctor_create_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_days'] = list(range(0, 7))

        return context

    def post(self, request, *args, **kwargs):
        days_times = []

        day_add = request.POST['day_select']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        invalid = False
        if start_time == '' or end_time == '':
            invalid = True

        doctor = request.user.doctor
        days = self.model.objects.filter(doctor_id=doctor.id).order_by('day')

        add_day_to_bd = True

        day_obj = None

        for d in days:
            if d.day == int(day_add):
                day_obj = d
                add_day_to_bd = False
                break

        if add_day_to_bd and not invalid:
            obj = DaySchedule(day=day_add, doctor_id=doctor.id)
            obj.save()
            day_obj = obj

        if not invalid:
            start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
            end_time = datetime.datetime.strptime(end_time, '%H:%M').time()
            obj = TimeSchedule(start_time=start_time, end_time=end_time, day_id=day_obj.id)

        days = self.model.objects.filter(doctor_id=doctor.id).order_by('day')
        add_ts_to_bd = True
        for d in days:
            daytime = Schedule(d)
            daytime.times = TimeSchedule.objects.filter(day_id=d.id).order_by('start_time')
            if d.day == int(day_add) and not invalid:
                for ts in daytime.times:
                    if ts.start_time == obj.start_time and ts.end_time == obj.end_time:
                        add_ts_to_bd = False
            days_times.append(daytime)
        if add_ts_to_bd and not invalid:
            obj.save()
            days_times = []
            for d in days:
                daytime = Schedule(d)
                daytime.times = TimeSchedule.objects.filter(day_id=d.id).order_by('start_time')
                days_times.append(daytime)

        return HttpResponseRedirect(self.success_url)


@method_decorator(doctor_required, name='dispatch')
class DoctorScheduleDelete(PermissionRequiredMixin, DeleteView):
    model = DaySchedule
    context_object_name = 'days_times'
    template_name = 'dash/doctor_schedule.html'
    success_url = reverse_lazy('doctor-schedule')
    permission_required = 'dash.delete_dayschedule'

    def get(self, request, *args, **kwargs):
        ds_id = kwargs['ds_id']
        ts_id = kwargs['ts_id']

        TimeSchedule.objects.filter(id=ts_id).delete()

        if not TimeSchedule.objects.filter(day_id=ds_id):
            DaySchedule.objects.filter(id=ds_id).delete()

        return HttpResponseRedirect(self.success_url)

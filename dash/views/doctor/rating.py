from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from dash.decorators import doctor_required
from django.urls import reverse_lazy
from django.shortcuts import render
from dash.models import Rating
from dash.models import DaySchedule
from dash.models import TimeSchedule
import datetime

@method_decorator(doctor_required, name='dispatch')
class RatingListView(PermissionRequiredMixin, TemplateView):
    model = Rating
    context_object_name = 'ratings'
    template_name = 'dash/ratings.html'
    permission_required = "dash.view_rating"

    def get_context_data(self, **kwargs):
        # Joao Pedro.

        #context = super().get_context_data(**kwargs)
        #context[self.context_object_name] = self.model.objects\
        #    .filter()\
        #    .order_by('appointment__datetime')

        doctor = self.request.user.doctor
        context = {self.context_object_name: self.model.objects
                                                .filter(appointment__doctor_id=doctor.id)
                                                .order_by('-appointment__datetime')}
        context['is_doctor'] = True
        return context

class Schedule:
    def __init__(self, day):
        self.day = day
        self.times = []


@method_decorator(doctor_required, name='dispatch')
class DoctorSchedule(PermissionRequiredMixin, TemplateView):
    model = DaySchedule
    context_object_name = 'days_times'
    template_name = 'dash/doctor_schedule.html'
    permission_required = "dash.view_rating"

    def get_context_data(self, **kwargs):
        # Joao Pedro.
        days_times = []

        doctor = self.request.user.doctor
        days = self.model.objects.filter(doctor_id=doctor.id).order_by('day')

        for d in days:
            daytime = Schedule(d)
            daytime.times = TimeSchedule.objects.filter(day_id=d.id).order_by('start_time')
            days_times.append(daytime)

        context = {self.context_object_name: days_times}
        context['is_doctor'] = True
        context['all_days'] = {0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira', 3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado', 6: 'Domingo'}
        return context


@method_decorator(doctor_required, name='dispatch')
class DoctorCreateSchedule(PermissionRequiredMixin, TemplateView):
    model = DaySchedule
    context_object_name = 'days_times'
    template_name = 'dash/doctor_create_schedule.html'
    permission_required = "dash.view_rating"

    def get_context_data(self, **kwargs):
        context = {}
        context['is_doctor'] = True
        context['all_days'] = {0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira', 3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado', 6: 'Domingo'}
        return context


@method_decorator(doctor_required, name='dispatch')
class DoctorScheduleAdd(PermissionRequiredMixin, TemplateView):
    model = DaySchedule
    context_object_name = 'days_times'
    template_name = 'dash/doctor_schedule.html'
    permission_required = "dash.view_rating"

    def post(self, request, *args, **kwargs):
        # Joao Pedro.
        days_times = []

        day_add = self.request.POST['day_select']
        start_time = self.request.POST['start_time']
        end_time = self.request.POST['end_time']

        invalid = False
        if start_time == '' or end_time == '':
            invalid = True

        doctor = self.request.user.doctor
        days = self.model.objects.filter(doctor_id=doctor.id).order_by('day')

        add_day_to_bd = True
        
        day_obj = None

        for d in days:
            if d.day == int(day_add):
                day_obj = d
                add_day_to_bd = False
                break

        if add_day_to_bd and not invalid:
            # Adiciona dayschedule ao banco de dados:
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

        context = {self.context_object_name: days_times}
        context['is_doctor'] = True
        context['all_days'] = {0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira', 3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado', 6: 'Domingo'}
        return HttpResponseRedirect("../schedule")


@method_decorator(doctor_required, name='dispatch')
class DoctorScheduleDelete(PermissionRequiredMixin, TemplateView):
    model = DaySchedule
    context_object_name = 'days_times'
    template_name = 'dash/doctor_schedule.html'
    permission_required = "dash.view_rating"

    def get_context_data(self, **kwargs):
        # Joao Pedro.
        days_times = []

        ds_id = kwargs['ds_id']
        ts_id = kwargs['ts_id']

        # deleta timeschedule:
        TimeSchedule.objects.filter(id=ts_id).delete()

        # se nao tem mais timeschedules para o dayschedule, deleta tbm:
        if not TimeSchedule.objects.filter(day_id=ds_id):
            DaySchedule.objects.filter(id=ds_id).delete()

        doctor = self.request.user.doctor
        days = self.model.objects.filter(doctor_id=doctor.id).order_by('day')

        for d in days:
            daytime = Schedule(d)
            daytime.times = TimeSchedule.objects.filter(day_id=d.id).order_by('start_time')
            days_times.append(daytime)

        context = {self.context_object_name: days_times}
        context['is_doctor'] = True
        context['all_days'] = {0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira', 3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado', 6: 'Domingo'}
        return context
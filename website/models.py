from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Address(models.Model):
    uf = models.CharField(max_length=2)
    city = models.CharField(max_length=40)
    neighborhood = models.CharField(max_length=40)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=6)
    complement = models.CharField(max_length=15, null=True)


class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)


class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    address = models.OneToOneField(Address, on_delete=models.PROTECT)
    crm = models.CharField(max_length=6)
    crm_uf = models.CharField(max_length=2)
    speciality = models.CharField(max_length=25)
    avg_rating = models.FloatField()

    def get_free_schedule(self, startdt, enddt):
        appointments = list(self.appointment_set.filter(datetime__range=(startdt, enddt)))
        dayschedules = list(self.dayschedule_set)

        # Gera todos datetimes entre startdt e enddt:
        datetimes = [startdt]
        curr_datetime = startdt
        while curr_datetime < enddt:
            curr_datetime += timedelta(minutes = 30)
            datetimes.append(curr_datetime)

        # Remove datetimes que ja estao associados a consultas:
        for a in appointments:
            if a.datetime in datetimes:
                datetimes.remove(a.datetime)

        # Remove datetimes em que o doutor nao atende:

        # dias da semana:
        dayschedules_weekdays = [d.day for d in dayschedules]
        for d in datetimes:
            if d.weekday() not in dayshedules_weekdays:
                datetimes.remove(d)

        # horarios:
        for ds in dayschedules:
            timeschedules = list(ds.timeschedule_set)  # timeschedules do dayschedule.
            dt = [d for d in datetimes if d.weekday() == ds.day]  # datetimes com dia da semana igual ao dayschedule.

            for d in dt:
                remover = True
                for ts in timeschedules:
                    # se existe um timeschedule onde d se encaixa:
                    if d.hour > ts.start_time.hour and  d.hour < ts.end_time.hour:
                        remover = False
                    if d.hour == ts.start_time.hour:
                        if d.minute >= ts.start_time.minute:
                            remover = False
                    if d.hour == ts.end_time.hour:
                        if d.minute <= ts.end_time.minute:
                            remover = False
                    if not remover:
                        break
                if remover:
                    datetimes.remove(d)
        return datetimes   
        

    def has_free_schedule(self, startdt, enddt):
        return len(get_free_schedule)


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    address = models.OneToOneField(Address, on_delete=models.PROTECT)
    cpf = models.CharField(max_length=11)
    birth_date = models.DateField()


class Rating(models.Model):
    REALLY_BAD = 0
    BAD = 1
    NEUTRAL = 2
    GOOD = 3
    VERY_GOOD = 4
    EXCELLENT = 5

    STARS_CHOICES = (
        (REALLY_BAD, 'Muito ruim'),
        (BAD, 'Ruim'),
        (NEUTRAL, 'Indiferente'),
        (GOOD, 'Bom'),
        (VERY_GOOD, 'Muito bom'),
        (EXCELLENT, 'Excelente')
    )

    WAITING = 'W'
    NOT_APPROVED = 'N'
    APPROVED = 'A'

    STATUS_CHOICES = (
        (WAITING, 'Esperando pela aprovação'),
        (NOT_APPROVED, 'Não aprovado'),
        (APPROVED, 'Aprovado')
    )

    description = models.TextField()
    stars = models.PositiveSmallIntegerField(choices=STARS_CHOICES, default=NEUTRAL)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=WAITING)


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE, null=True)
    datetime = models.DateTimeField()


class DaySchedule(models.Model):
    SUNDAY = 6
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5

    DAY_CHOICES = (
        (SUNDAY, 'Domingo'),
        (MONDAY, 'Segunda-feira'),
        (TUESDAY, 'Terça-feira'),
        (WEDNESDAY, 'Quarta-feira'),
        (THURSDAY, 'Quinta-feira'),
        (FRIDAY, 'Sexta-feira'),
        (SATURDAY, 'Sábado')
    )

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField(choices=DAY_CHOICES)


class TimeSchedule(models.Model):
    day = models.ForeignKey(DaySchedule, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

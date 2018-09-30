from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class Address(models.Model):
    uf = models.CharField(max_length=2)
    city = models.CharField(max_length=40)
    neighborhood = models.CharField(max_length=40)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=6)
    complement = models.CharField(max_length=15, null=True)

    def __str__(self):
        if self.complement is not None:
            return "{} {}, {}, {} - {}/{}".format(self.street,
                                                  self.number,
                                                  self.complement,
                                                  self.neighborhood,
                                                  self.city,
                                                  self.uf)

        return "{} {}, {} - {}/{}".format(self.street, self.number, self.neighborhood, self.city, self.uf)


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
        appointments = self.appointment_set.filter(datetime__range=(startdt, enddt))
        dayschedules = self.dayschedule_set.all()

        startdt_min = startdt.minute if startdt.minute in [0, 30] else startdt.minute + (30 - startdt.minute)
        enddt_min = enddt.minute if enddt.minute in [0, 30] else enddt.minute + (30 - enddt.minute)

        startdt = datetime(startdt.year, startdt.month, startdt.day, startdt.hour, startdt_min, 0, 0)
        enddt = datetime(enddt.year, enddt.month, enddt.day, enddt.hour, enddt_min, 0, 0)

        # Gera todos datetimes entre startdt e enddt:
        datetimes = [startdt]
        curr_datetime = startdt
        while curr_datetime < enddt:
            curr_datetime += timedelta(minutes=30)
            datetimes.append(curr_datetime)

        # Remove datetimes que ja estao associados a consultas:
        for a in appointments:
            if a.datetime in datetimes:
                datetimes.remove(a.datetime)

        # Remove datetimes em que o doutor nao atende:
        # dias da semana:
        dayschedules_weekdays = [d.day for d in dayschedules]
        datetimes = [d for d in datetimes if d.weekday() in dayschedules_weekdays]

        # horarios:
        for ds in dayschedules:
            timeschedules = ds.timeschedule_set.all()  # timeschedules do dayschedule.
            dt = [d for d in datetimes if d.weekday() == ds.day]  # datetimes com dia da semana igual ao dayschedule.

            for d in dt:
                it_fits = []

                for ts in timeschedules:
                    # se existe um timeschedule onde d se encaixa:
                    it_fits.append(ts.start_time <= d.time() <= ts.end_time)

                if not any(it_fits):
                    # Nao encaixou com nenhum intervalo
                    datetimes.remove(d)

        return datetimes

    def has_free_schedule(self, startdt, enddt):
        return len(self.get_free_schedule(startdt, enddt))


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

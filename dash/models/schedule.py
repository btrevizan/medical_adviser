from django.db import models
from .users import Doctor


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

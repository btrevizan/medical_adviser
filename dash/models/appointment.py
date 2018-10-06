from django.db import models
from .users import Doctor, Patient


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

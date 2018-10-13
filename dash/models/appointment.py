from django.db import models
from .users import Doctor, Patient


class Appointment(models.Model):
    CREDIT_CARD = 'C'
    HEALTH_INSURANCE = 'H'

    PAYMENT_METHODS = (
        (CREDIT_CARD, 'Cartão de Crédito'),
        (HEALTH_INSURANCE, 'Plano de Saúde')
    )

    CONFIRMED = 'C'
    WAITING = 'W'

    STATUS_CHOICES = (
        (CONFIRMED, 'Confirmada.'),
        (WAITING, 'Aguardando confirmação.')
    )

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='W')
    datetime = models.DateTimeField()

    def is_payment_method_valid(self):
        # TODO: integrate with credit card/health insurance systems to check
        return self.payment_method in list(zip(*self.PAYMENT_METHODS)[0])

    def confirm(self, commit=True):
        """Set status as CONFIRMED.

        :param commit: bool
            Whether to save in database.
        """
        self.status = self.CONFIRMED

        if commit:
            self.save()


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
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True)

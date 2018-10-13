import numpy as np
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.PROTECT)
    crm = models.CharField(max_length=6)
    crm_uf = models.CharField(max_length=2)
    description = models.TextField(null=True)
    speciality = models.CharField(max_length=25)
    avg_rating = models.FloatField(default=0)

    def get_free_schedule(self, startdt, enddt):
        """Get datetime not used in appointments.

        :param startdt: datetime
            Start interval's datetime.

        :param enddt: datetime
            End interval's datetime.

        :return: list
            A list of datetime objects.
        """
        appointments = self.appointment_set.filter(datetime__range=(startdt, enddt))
        dayschedules = self.dayschedule_set.all()

        # Fix minute to 0 or 30
        startdt_min = startdt.minute if startdt.minute in [0, 30] else startdt.minute + (30 - startdt.minute)
        enddt_min = enddt.minute if enddt.minute in [0, 30] else enddt.minute + (30 - enddt.minute)

        # Fixed limits
        startdt = datetime(startdt.year, startdt.month, startdt.day, startdt.hour, startdt_min, 0, 0)
        enddt = datetime(enddt.year, enddt.month, enddt.day, enddt.hour, enddt_min, 0, 0)

        # Create datetimes between startdt and enddt
        datetimes = [startdt]
        curr_datetime = startdt
        while curr_datetime < enddt:
            curr_datetime += timedelta(minutes=30)
            datetimes.append(curr_datetime)

        # Removed used datetimes (has appointments)
        for a in appointments:
            if a.datetime in datetimes:
                datetimes.remove(a.datetime)

        # Remove datetimes that are not in business hours
        dayschedules_weekdays = [d.day for d in dayschedules]
        datetimes = [d for d in datetimes if d.weekday() in dayschedules_weekdays]

        for ds in dayschedules:
            # Timeschedules do dayschedule.
            timeschedules = ds.timeschedule_set.all()

            # Datetimes with equal weekday of dayschedule
            dt = [d for d in datetimes if d.weekday() == ds.day]

            for d in dt:
                it_fits = []

                for ts in timeschedules:
                    # If exists a timeschedule which d fits in
                    it_fits.append(ts.start_time <= d.time() <= ts.end_time)

                if not any(it_fits):
                    # Did not fitted on any timeschedule
                    datetimes.remove(d)

        return datetimes

    def has_free_schedule(self, startdt, enddt):
        """Check whether the doctor has a free datetime in his schedule in some interval.

        :param startdt: datetime
            Start interval's datetime.

        :param enddt: datetime
            End interval's datetime.

        :return: bool
            Whether the doctor has some datetime not used in appointments.
        """
        return len(self.get_free_schedule(startdt, enddt))

    def update_avg_rating(self, commit=True):
        """Update doctor's average rating.

        :param startdt: bool (default True)
            Whether to save the object in database.
        """
        ratings = [a.rating.stars for a in self.appointment_set.filter(rating__isnull=False)]
        avg_rating = np.mean(ratings)

        self.avg_rating = avg_rating

        if commit:
            self.save()


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)
    uf = models.CharField(max_length=2)
    city = models.CharField(max_length=70)

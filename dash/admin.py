from django.contrib import admin

# Register your models here.

from . models import Appointment, Rating, DaySchedule, TimeSchedule, Address, Admin, Doctor, Patient
 
admin.site.register(Appointment)
admin.site.register(Rating)
admin.site.register(DaySchedule)
admin.site.register(TimeSchedule)
admin.site.register(Address)
admin.site.register(Admin)
admin.site.register(Doctor)
admin.site.register(Patient)

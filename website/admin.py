from django.contrib import admin
from .models import *


admin.site.register(Admin)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Rating)
admin.site.register(Appointment)
admin.site.register(DaySchedule)


from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('appointment/create/', views.AppointmentCreateView.as_view(), name='create_appointment'),
    path('appointment/create/success', views.AppointmentCreateSuccessView.as_view(), name='create_appointment_success')
]
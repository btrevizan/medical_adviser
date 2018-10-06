from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('appointment/create/', views.AppointmentCreateView.as_view(), name='create_appointment'),
    path('appointment/create/success', views.AppointmentCreateSuccessView.as_view(), name='create_appointment_success'),
    path('search', views.SearchDoctorView.as_view(), name='search'),
    path('doctor/<int:pk>/profile', views.DoctorProfileView.as_view(), name='doctor_profile')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

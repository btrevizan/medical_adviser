from django.conf.urls.static import static
from django.urls import include, path
from django.conf import settings
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup', views.SignUpView.as_view(), name='sign_up'),
    path('signup/patient', views.SignUpPatientView.as_view(), name='sign_up_patient'),
    path('signup/doctor', views.SignUpDoctorView.as_view(), name='sign_up_doctor'),
    path('logout/success', views.LogoutView.as_view(), name='logout')
    # path('doctor/<int:pk>/profile', views.DoctorProfileView.as_view(), name='doctor_profile')
]

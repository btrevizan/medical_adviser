from django.urls import include, path
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.DashView.as_view(), name='dash-redirect'),
    path('signup', views.SignUpView.as_view(), name='sign_up'),
    path('signup/patient', views.SignUpPatientView.as_view(), name='sign_up_patient'),
    path('signup/doctor', views.SignUpDoctorView.as_view(), name='sign_up_doctor'),
    path('logout/success', views.LogoutView.as_view(), name='logout'),

    path('patient/ratings', views.patient.RatingListView.as_view(), name='rating-list'),
    path('patient/ratings/change/<int:pk>', views.patient.RatingUpdateView.as_view(), name='rating-update'),
    path('patient/ratings/delete/<int:pk>', views.patient.RatingDeleteView.as_view(), name='rating-delete'),
    path('patient/appointments', views.patient.AppointmentListView.as_view(), name='appointment-list'),
    path('patient/appointments/rate/<int:pk>', views.patient.RatingCreateView.as_view(), name='rating-create'),
    path('patient/appointments/detail/<int:pk>', views.patient.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('patient/appointments/delete/<int:pk>', views.patient.AppointmentDeleteView.as_view(), name='appointment-delete'),

    path('admin/ratings', views.admin.RatingListView.as_view(), name='rating-list-admin'),
    path('admin/ratings/<int:pk>/<str:status>', views.admin.RatingUpdateView.as_view(), name='rating-update-admin'),
    path('admin/register', views.admin.RegisterAdminView.as_view(), name='register-admin'),

    path('doctor/ratings', views.doctor.RatingListView.as_view(), name='rating-list-doctor'),

    path('doctor/schedule', views.doctor.DoctorSchedule.as_view(), name='doctor-schedule'),
    path('doctor/schedule/create', views.doctor.DoctorCreateSchedule.as_view(), name='doctor-create-schedule'),    
    path('doctor/schedule/delete/<int:ds_id>/<int:ts_id>', views.doctor.DoctorScheduleDelete.as_view(), name='doctor-delete-schedule'),
]


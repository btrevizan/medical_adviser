from django.urls import include, path
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.DashRedirectView.as_view(), name='dash-redirect'),
    path('signup', views.SignUpView.as_view(), name='sign_up'),
    path('signup/patient', views.SignUpPatientView.as_view(), name='sign_up_patient'),
    path('signup/doctor', views.SignUpDoctorView.as_view(), name='sign_up_doctor'),
    path('logout/success', views.LogoutView.as_view(), name='logout'),
    path('ratings', views.RatingListView.as_view(), name='rating-list'),
    path('ratings/change/<int:pk>', views.RatingUpdateView.as_view(), name='rating-update'),
    path('ratings/delete/<int:pk>', views.RatingDeleteView.as_view(), name='rating-delete'),
    path('appointments', views.AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/rate/<int:pk>', views.RatingCreateView.as_view(), name='rating-create'),
    path('appointments/detail/<int:pk>', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/delete/<int:pk>', views.AppointmentDeleteView.as_view(), name='appointment-delete')
]


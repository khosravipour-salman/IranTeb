from django.urls import path
from patients import views


urlpatterns = [
    path('num-active-user/',views.NumActiveUser.as_view()),
    path('num-success-reserved/',views.NumSuccessfulReseced.as_view()),
    path('percent-satisfy/',views.UserSatisfy.as_view()),
    path('reserve-appointment/<int:pk>/',views.PatientReserveAppointment.as_view()),
    path('my-doctor/<int:pk>/',views.MyDoctor.as_view()),

]

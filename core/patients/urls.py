from django.urls import path
from patients import views

# from azbankgateways.urls import az_bank_gateways_urls


urlpatterns = [
    path('num-active-user/',views.NumActiveUser.as_view()),
    path('num-success-reserved/',views.NumSuccessfulReseced.as_view()),
    path('percent-satisfy/',views.UserSatisfy.as_view()),
    path('reserve-appointment/<int:pk>/',views.PatientReserveAppointment.as_view(),name='reserve-appointment'),
    path('my-doctor/<int:pk>/',views.MyDoctor.as_view()),
    path('doctor-free-appointment/<int:pk>/',views.DoctorFreeAppointment.as_view()),
    path('rserve-appointment-by-patient/<int:u_id>/<int:dr_id>/',views.RserveAppointmentByPatient.as_view()),
    path('cancel-appointment-by-patient/<int:u_id>/<int:dr_id>/',views.CancelAppointmentByPatient.as_view()),


    # path('bankgateways/', az_bank_gateways_urls()),
    # path('go-to-gateway/',views.go_to_gateway_view),
    # path('callback-gateway/',views.callback_gateway_view),

]

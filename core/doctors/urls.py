from django.urls import path,include
from doctors import views

app_name='doctor'

urlpatterns = [
    path('active-doctor-user',views.NumActiveDoctor.as_view()),
    path('recent-comment',views.RecentComment.as_view()),
    path('comment-for-doctor/<int:pk>',views.CommentForOneDoctor.as_view()),
    path('top-doctors',views.TopDoctors.as_view()),
    path('all-specialist/',views.All_Specialist.as_view()),
    path('doctors-list/',views.DoctorsList.as_view()),
    path('doctor-detail/<int:pk>',views.DoctorDetail.as_view(),name='doctor-detail'),
    path('doctor-advance-search/',views.DoctorAdvanceSearch.as_view()),
    path('doctor-reserve-apointment/<int:pk>',views.DoctorReserveApointment.as_view()),
    path('dr-register-informations/<int:pk>',views.DrRegisterInformations.as_view()),
    path('doctor-validate-phone-send-otp/',views.DoctorValidatePhoneSendOTP.as_view()),
    path('dr-verify-otp/',views.DrVerifyOTP.as_view()),
    path('doctor-address/<int:pk>',views.DoctorAddressInfo.as_view()),
    path('doctor-Tellphone/<int:dr_pk>/<int:t_pk>',views.DoctorTellphone.as_view()),
    path('doctor-complete-info/<int:pk>/',views.DrCompleteInfo.as_view()),

]
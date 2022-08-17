from django.urls import path,include
from doctors import views


urlpatterns = [
    path('active-doctor-user',views.NumActiveDoctor.as_view()),
    path('recent-comment',views.RecentComment.as_view()),
    path('top-doctors',views.TopDoctors.as_view()),
    path('all-specialist/',views.All_Specialist.as_view()),
    path('doctors-list/',views.DoctorsList.as_view()),
    path('doctors-detail/<int:u_id>',views.DoctorDetail.as_view()),

]
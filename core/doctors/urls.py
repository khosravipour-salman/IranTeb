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

]
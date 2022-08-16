from django.urls import path,include
from doctors import views


urlpatterns = [
    path('active-doctor-user',views.NumActiveDoctor.as_view()),
    path('recent-comment',views.RecentComment.as_view()),
    path('top-doctors',views.TopDoctors.as_view()),
    path('all-specialist/',views.All_Specialist.as_view()),
]
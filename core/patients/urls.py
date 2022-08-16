from django.urls import path
from patients import views
urlpatterns = [
    path('num-active-user',views.NumActiveUser.as_view()),
]

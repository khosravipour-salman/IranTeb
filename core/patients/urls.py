from django.urls import path
from patients import views

from azbankgateways.urls import az_bank_gateways_urls


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('num-active-user', views.NumActiveUser.as_view()),
    path('num-success-reserved/', views.NumSuccessfulReseced.as_view()),
    path('percent-satisfy/', views.UserSatisfy.as_view()),
    path('reserved/<int:pk>/', views.ReservedAppointment.as_view()),
    path('my-wallet/<int:pk>/', views.MyWallet.as_view()),
    path('patient-info/<int:pk>/', views.PatientInfo.as_view()),

    path('register-patient/', views.RegisterView.as_view()),
    path('get-patient-token/', views.GetTokenView.as_view()),
    path('patient/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('patient/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('bankgateways/', az_bank_gateways_urls()),
    path('go-to-gateway/', views.go_to_gateway_view),
    path('callback-gateway/', views.callback_gateway_view),
]

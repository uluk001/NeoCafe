from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.views import (
    ClientConfirmPhoneNumberView,
    ClientEditProfileView,
    ClientBirthDateView,
    RegisterView,
    LoginView,
    ResendCodeView,
    CheckPreToken
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view()),
    path("api/refresh/", TokenRefreshView.as_view()),
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("confirm-phone-number/", ClientConfirmPhoneNumberView.as_view()),
    path("birth-date/", ClientBirthDateView.as_view()),
    path("edit-profile/", ClientEditProfileView.as_view()),
    path("resend-code/", ResendCodeView.as_view()),
]

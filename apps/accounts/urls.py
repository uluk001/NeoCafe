from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import (
    ClientConfirmPhoneNumberView,
    ClientEditProfileView,
    ClientBirthDateView,
    RegisterView,
    LoginView,
    ResendCodeView,
    ClientConfirmLoginView,
    ClientUserProfileView,
)

urlpatterns = [
    path("api/refresh/", TokenRefreshView.as_view()),
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("confirm-phone-number/", ClientConfirmPhoneNumberView.as_view()),
    path("birth-date/", ClientBirthDateView.as_view()),
    path("edit-profile/", ClientEditProfileView.as_view()),
    path("resend-code/", ResendCodeView.as_view()),
    path("confirm-login/", ClientConfirmLoginView.as_view()),
    path("my-profile/", ClientUserProfileView.as_view()),
]

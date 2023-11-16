from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import (
    ClientBirthDateView,
    ClientConfirmLoginView,
    ClientConfirmPhoneNumberView,
    ClientEditProfileView,
    ClientUserProfileView,
    LoginView,
    RegisterView,
    ResendCodeView,
    AdminLoginView,
    LoginForClientView,
    TemporaryLoginView,
)

urlpatterns = [
    path("refresh/", TokenRefreshView.as_view()),  # accounts/refresh/
    path("register/", RegisterView.as_view()),  # accounts/register/
    path("login/", LoginView.as_view()),  # accounts/login/
    path(
        "confirm-phone-number/", ClientConfirmPhoneNumberView.as_view()
    ),  # accounts/confirm-phone-number/
    path("birth-date/", ClientBirthDateView.as_view()),  # accounts/birth-date/
    path("edit-profile/", ClientEditProfileView.as_view()),  # accounts/edit-profile/
    path("resend-code/", ResendCodeView.as_view()),  # accounts/resend-code/
    path("confirm-login/", ClientConfirmLoginView.as_view()),  # accounts/confirm-login/
    path("my-profile/", ClientUserProfileView.as_view()),  # accounts/my-profile/
    path("admin-login/", AdminLoginView.as_view()),  # accounts/admin-login/
    path(
        "login-for-client/", LoginForClientView.as_view()
    ),  # accounts/login-for-client/
    path(
        "temporary-login/", TemporaryLoginView.as_view()
    ),  # accounts/temporary-login/
]

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import (
    AdminLoginView, ClientBirthDateView,
    ClientConfirmLoginView, ClientConfirmPhoneNumberView,
    ClientEditProfileView, ClientUserProfileView,
    LoginForClientView, LoginView, RegisterView,
    ResendCodeView, ResendCodeWithPreTokenView,
    TemporaryLoginView, WaiterLoginView,
    WaiterTemporaryLoginView, EmployeeScheduleView,
    UpdateWaiterProfileView,
)

urlpatterns = [
    path("refresh/", TokenRefreshView.as_view()),  # accounts/refresh/
    path("register/", RegisterView.as_view()),  # accounts/register/
    path(
        "confirm-phone-number/", ClientConfirmPhoneNumberView.as_view()
    ),  # accounts/confirm-phone-number/
    path("birth-date/", ClientBirthDateView.as_view()),  # accounts/birth-date/
    path("edit-profile/", ClientEditProfileView.as_view()),  # accounts/edit-profile/
    path("resend-code/", ResendCodeView.as_view()),  # accounts/resend-code/
    path(
        "resend-code-with-pre-token/", ResendCodeWithPreTokenView.as_view()
    ),  # accounts/resend-code-with-per-token/
    path("my-profile/", ClientUserProfileView.as_view()),  # accounts/my-profile/
    path("confirm-login/", ClientConfirmLoginView.as_view()),  # accounts/confirm-login/
    path("admin-login/", AdminLoginView.as_view()),  # accounts/admin-login/
    path("login/", LoginView.as_view()),  # accounts/login/
    path(
        "login-for-client/", LoginForClientView.as_view()
    ),  # accounts/login-for-client/
    path("login-waiter/", WaiterLoginView.as_view()),  # accounts/login-waiter/
    path("temporary-login/", TemporaryLoginView.as_view()),  # accounts/temporary-login/
    path(
        "temporary-login-waiter/", WaiterTemporaryLoginView.as_view()
    ),  # accounts/temporary-login-waiter/

    path("my-schedule/", EmployeeScheduleView.as_view()),  # accounts/employee-schedule/
    path("update-waiter-profile/", UpdateWaiterProfileView.as_view()),  # accounts/update-waiter-profile/
]

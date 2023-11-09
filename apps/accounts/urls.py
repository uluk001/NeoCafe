# from django.urls import include, path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from accounts.views import (
#     PhoneNumberVerificationView,
#     SendPhoneNumberVerificationView,
#     UserProfileViewSet,
#     EditProfileView,
#     ChangePasswordView,
#     SendCodeForChangePhoneNumber,
#     ChangePhoneNumberView,
#     SendVerificationCodeForResetPassword,
#     ResetPasswordView,
#     GetVerificationCodeForResetPassword,
# )

# urlpatterns = [
#     path("profile/", UserProfileViewSet.as_view()),
#     path("login/", TokenObtainPairView.as_view()),
#     path("api/refresh/", TokenRefreshView.as_view()),
#     path("send_phone_number/", SendPhoneNumberVerificationView.as_view()),
#     path("confirm_phone_number/", PhoneNumberVerificationView.as_view()),
#     path("edit_profile/", EditProfileView.as_view()),
#     path("change_password/", ChangePasswordView.as_view()),
#     path('send_code_for_change_phone_number/', SendCodeForChangePhoneNumber.as_view()),
#     path('change_phone_number/', ChangePhoneNumberView.as_view()),
#     path('send_verification_code_for_reset_password/', SendVerificationCodeForResetPassword.as_view()),
#     path('reset_password/', ResetPasswordView.as_view()),
#     path('get_verification_code_for_reset_password/', GetVerificationCodeForResetPassword.as_view()),
# ]

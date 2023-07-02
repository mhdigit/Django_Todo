from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # =============== registration ============================
    path(
        "registration/",
        views.RegistrationApiView.as_view(),
        name="registration",
    ),

    path(
        "register/email-verify/",
        views.VerifyEmailApiView.as_view(),
        name="email_verify"
    ),
    path(
        "register/email-verify/resend/",
        views.ResendVerifyEmailApiView.as_view(),
        name="email_verify_resend"
    ),
    # ================ change password ==================================
    path(
        "change-password/",
        views.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # =============== reset password ========================================
    path(
        "reset-password/",
        views.PasswordResetRequestEmailApiView.as_view(),
        name="reset-password-request"
    ),
    path(
        "reset-password/validate-token/",
        views.PasswordResetTokenValidateApiView.as_view(),
        name="reset-password-validate"
    ),

    path(
        "reset-password/set-password/",
        views.PasswordResetSetNewApiView.as_view(),
        name="reset-password-confirm"
    ),

    # =============== login token =========================================
    path(
        "token/login/",
        views.CustomObtainAuthToken.as_view(),
        name="token-login",
    ),
    path(
        "token/logout/",
        views.CustomDiscardAuthToken.as_view(),
        name="token-logout",
    ),
    # ================= login jwt ==============================================
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    # ================== profile ================================================
    path("profile/", views.ProfileApiView.as_view(), name="profile"),
    # ================== test email =================================
    path("test-email", views.TestEmailSend.as_view(), name="test-email"),
]

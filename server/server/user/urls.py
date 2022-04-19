from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from user.api import (
    SearchView,
    UploadAvatar,
    UserViewSet,
    ObtainTokenPairView,
    Register,
    LogoutAndBlacklistRefreshTokenForUserView,
    ConfirmEmail,
    ConfirmSecondaryEmail,
    ResendOtp,
    SecondaryEmailResendOtp,
    PasswordResetEmailView,
    PasswordResetView,
    PasswordChangeView,
    UserEmailViewSet,
    OtpExpireTimer,
    GetSpaceName
)

router = routers.DefaultRouter()
router.register('', UserViewSet, 'user')

secondary_email = UserEmailViewSet.as_view({'get': 'lists', 'post': 'create'})
secondary_email_detail = UserEmailViewSet.as_view({'delete': 'destroy'})

urlpatterns = [
    path('avatar/', UploadAvatar.as_view(), name="avatar"),
    path('spacename/', GetSpaceName.as_view(), name="SpaceName"),
    path('register/', Register.as_view()),
    path('confirmEmail/', ConfirmEmail.as_view(), name="confirm_email"),
    path('confirmSecondaryEmail/', ConfirmSecondaryEmail.as_view(), name="confirm_secondary_email"),
    path('userEmail/', secondary_email, name="secondary_email"),
    path('userEmail/<int:id>/', secondary_email_detail, name="secondary_email_detail"),
    path('resendOtp/', ResendOtp.as_view(), name="resend_otp"),
    path('secondaryEmailResendOtp/', SecondaryEmailResendOtp.as_view(), name="secondary_email_resend_otp"),
    path('otpExpireTimer/', OtpExpireTimer.as_view(), name="otpExpireTimer"),
    path('login/', ObtainTokenPairView.as_view(), name='login'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAndBlacklistRefreshTokenForUserView.as_view(),    name='blacklist'),
    path('forgot_password/', PasswordResetEmailView.as_view({'post': 'send'})),
    path('reset_password/', PasswordResetView.as_view({'post': 'reset'})),
    path('change_password/', PasswordChangeView.as_view({'post': 'reset'})),
    path('search/', SearchView.as_view()),
    path("", include(router.urls)),
]

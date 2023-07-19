from django.urls import path
from accounts.views.authentication import (
    RegisterUserView,
    VerifyUserView,
    LoginUserView,
    ResendTokenView
)
from accounts.views.profile import ProfileView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name='register'),
    path("login/", LoginUserView.as_view(), name="login"),
    path(
        "verify/<str:verification_token>/<str:user_token>/",
        VerifyUserView.as_view(),
        name="verify"
    ),
    path("resend/", ResendTokenView.as_view(), name='resend_verification'),
    path("<str:user_token>/", ProfileView.as_view(), name='profile')
] 

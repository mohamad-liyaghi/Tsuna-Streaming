from django.urls import path
from accounts.views.authentication import (
    RegisterUserView, VerifyUserView, LoginUserView
)

app_name = "v1_accounts"

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name='register'),
    path("login/", LoginUserView.as_view(), name="login"),
    path("verify/<str:user_id>/<str:token>/", VerifyUserView.as_view(), name="verify")
]

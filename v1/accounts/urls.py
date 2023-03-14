from django.urls import path
from accounts.views.authentication import (
    RegisterUserView, VerifyUserView, LoginUserView
)
from accounts.views.profile import ProfileView

app_name = "v1_accounts"


urlpatterns = [
    path("register/", RegisterUserView.as_view(), name='register'),
    path("login/", LoginUserView.as_view(), name="login"),
    path("verify/<str:token>/<str:user_token>/", VerifyUserView.as_view(), name="verify"),
    path("profile/<str:token>/", ProfileView.as_view(), name='profile')
] 

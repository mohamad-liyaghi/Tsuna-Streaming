from django.urls import path
from accounts.views.authentication import (
    RegisterUserView, VerifyUserView
)

app_name = "v1_accounts"

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name='register'),
    path("verify/<str:user_id>/<str:token>/", VerifyUserView.as_view(), name="verify")
]

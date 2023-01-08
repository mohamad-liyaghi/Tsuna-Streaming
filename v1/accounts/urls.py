from django.urls import path
from accounts.views.authentication import (
    RegisterUserView
)

app_name = "v1_accounts"

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name='register')
]

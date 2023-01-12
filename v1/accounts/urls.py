from django.urls import path
from accounts.views.authentication import (
    RegisterUserView, VerifyUserView, LoginUserView
)
from accounts.views.profile import ProfileView
from accounts.views.subscription import SubscriptionViewSet
from rest_framework import routers

app_name = "v1_accounts"
router = routers.DefaultRouter()

router.register("subscription", SubscriptionViewSet, basename="subscription")

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name='register'),
    path("login/", LoginUserView.as_view(), name="login"),
    path("verify/<str:user_id>/<str:token>/", VerifyUserView.as_view(), name="verify"),
    path("profile/<int:user_id>/", ProfileView.as_view(), name='profile')
] 

urlpatterns += router.urls
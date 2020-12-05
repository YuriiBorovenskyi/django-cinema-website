from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.urls import path

from .views import (
    ChangeUserInfoView,
    DeleteUserView,
    ProfileView,
    RegisterDoneView,
    RegisterUserView,
    UserPasswordChangeView,
    UserPasswordResetCompleteView,
    UserPasswordResetConfirmView,
    UserPasswordResetDoneView,
    UserPasswordResetView,
    user_activate,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password/change/",
        UserPasswordChangeView.as_view(),
        name="password_change",
    ),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "profile/change/", ChangeUserInfoView.as_view(), name="profile_change"
    ),
    path("profile/delete/", DeleteUserView.as_view(), name="profile_delete"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("register/done/", RegisterDoneView.as_view(), name="register_done"),
    path(
        "register/activate/<str:sign>/", user_activate, name="register_activate"
    ),
    path(
        "password/reset/",
        UserPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password/reset/done/",
        UserPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password/confirm/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/confirm/complete/",
        UserPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

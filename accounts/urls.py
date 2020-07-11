from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView,\
    PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='registration/change_password.html'
    ), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(
        template_name='registration/password_changed.html'
    ), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(
        template_name='registration/reset_password.html',
        subject_template_name='registration/reset_subject.txt',
        email_template_name='registration/reset_email.html'
    ), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/email_sent.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/confirm_password.html'
    ), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='registration/password_confirmed.html'
    ), name='password_reset_complete'),
]

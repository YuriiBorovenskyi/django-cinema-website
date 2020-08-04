from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, \
    DeleteView

from .forms import ChangeUserInfoForm, RegisterUserForm
from .utilities import signer


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = "User's personal data has been changed."

    def dispatch(self, request, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserPasswordChangeView(
    SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView
):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = 'User password has been changed.'


class RegisterUserView(CreateView):
    model = User
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'registration/bad_signature.html')
    user = get_object_or_404(User, username=username)
    template = 'registration/activation_done.html'
    user.is_active = True
    user.save()
    return render(request, template)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'registration/delete_user.html'
    success_url = reverse_lazy('cinema:index-list')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS,
                             'User account has been deleted.')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    subject_template_name = 'email/reset_letter_subject.txt'
    email_template_name = 'email/reset_letter_body.txt'
    success_url = reverse_lazy('password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_complete.html'


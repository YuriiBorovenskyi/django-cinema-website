import pytest
from django.urls import reverse
from pytest_django.asserts import (
    assertRedirects,
    assertTemplateUsed,
)

from accounts.models import User


@pytest.mark.django_db
class TestProfileView:
    def test_view_url_exists_at_desired_location(
        self, client, create_logged_in_user
    ):
        response = client.get("/accounts/profile/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_logged_in_user):
        response = client.get(reverse("profile"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_logged_in_user):
        response = client.get(reverse("profile"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/profile.html")


@pytest.mark.django_db
class TestChangeUserInfoView:
    def test_view_url_exists_at_desired_location(
        self, client, create_logged_in_user
    ):
        response = client.get("/accounts/profile/change/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_logged_in_user):
        response = client.get(reverse("profile_change"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_logged_in_user):
        response = client.get(reverse("profile_change"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/change_user_info.html")

    def test_view_redirects_to_profile_url_after_getting_of_valid_form_data(
        self, client, create_logged_in_user
    ):
        form_data = {
            "username": "new_test_username",
            "email": "new.test.username@example.com",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        response = client.post(
            path=reverse("profile_change"),
            data=form_data,
        )
        assert response.status_code == 302
        assertRedirects(response, reverse("profile"))

        redirect_url = response.url
        next_response = client.get(redirect_url)

        assert next_response.status_code == 200
        assert next_response.context["user"].username == "new_test_username"

        for message in next_response.context["messages"]:
            if message.tags == "success":
                assert (
                    message.message == "User's personal data has been changed."
                )


@pytest.mark.django_db
class TestUserPasswordChangeView:
    def test_view_url_exists_at_desired_location(
        self, client, create_logged_in_user
    ):
        response = client.get("/accounts/password/change/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_logged_in_user):
        response = client.get(reverse("password_change"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_logged_in_user):
        response = client.get(reverse("password_change"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/password_change.html")

    def test_view_redirects_to_profile_url_after_getting_of_valid_form_data(
        self, client, create_logged_in_user
    ):
        old_hash_password = User.objects.get(username="test.username").password
        form_data = {
            "old_password": "test_password",
            "new_password1": "new_test_password",
            "new_password2": "new_test_password",
        }
        response = client.post(
            path=reverse("password_change"),
            data=form_data,
        )
        assert response.status_code == 302
        assertRedirects(response, reverse("profile"))

        redirect_url = response.url
        next_response = client.get(redirect_url)

        assert next_response.status_code == 200
        assert next_response.context["user"].password != old_hash_password

        for message in next_response.context["messages"]:
            if message.tags == "success":
                assert message.message == "User password has been changed."


@pytest.mark.django_db
class TestRegisterUserView:
    def test_view_url_exists_at_desired_location(self, client):
        response = client.get("/accounts/register/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client):
        response = client.get(reverse("register"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client):
        response = client.get(reverse("register"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/register_user.html")

    def test_view_redirects_to_register_done_url_after_getting_valid_form_data(
        self, client
    ):
        form_data = {
            "username": "test_username",
            "email": "test.username@example.com",
            "password1": "test_password",
            "password2": "test_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        response = client.post(
            path=reverse("register"),
            data=form_data,
        )
        assert response.status_code == 302
        assertRedirects(response, reverse("register_done"))

        redirect_url = response.url
        next_response = client.get(redirect_url)

        assert next_response.status_code == 200
        assert User.objects.get(username="test_username")


@pytest.mark.django_db
class TestUserActivate:
    url_pattern = "/accounts/register/activate/"
    sign = "test.username:X23J5EBDjDGDDwVphQDKHFP_i5S7eL-kg7Np6M5yOhA"

    def test_view_url_exists_at_desired_location(
        self, client, create_non_activated_user
    ):
        response = client.get(f"{self.url_pattern}{self.sign}/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(
        self, client, create_non_activated_user
    ):
        response = client.get(reverse("register_activate", args=(self.sign,)))
        assert response.status_code == 200

    def test_user_can_log_in_after_successful_activation(
        self, client, create_non_activated_user
    ):
        response = client.get(reverse("register_activate", args=(self.sign,)))
        assert response.status_code == 200
        assert client.login(username="test.username", password="test_password")
        assert User.objects.get(username="test.username").is_authenticated

    def test_view_uses_correct_template_if_successful_activation(
        self, client, create_non_activated_user
    ):
        response = client.get(reverse("register_activate", args=(self.sign,)))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/activation_done.html")

    def test_view_uses_correct_template_if_unsuccessful_activation(
        self, client, create_non_activated_user
    ):
        response = client.get(
            reverse("register_activate", args=(f"{self.sign}error",))
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/bad_signature.html")


@pytest.mark.django_db
class TestRegisterDoneView:
    def test_view_url_exists_at_desired_location(self, client):
        response = client.get("/accounts/register/done/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client):
        response = client.get(reverse("register_done"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client):
        response = client.get(reverse("register_done"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/register_done.html")


@pytest.mark.django_db
class TestDeleteUserView:
    def test_view_url_exists_at_desired_location(
        self, client, create_logged_in_user
    ):
        response = client.get("/accounts/profile/delete/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_logged_in_user):
        response = client.get(reverse("profile_delete"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_logged_in_user):
        response = client.get(reverse("profile_delete"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/delete_user.html")

    def test_view_redirects_to_login_url_if_user_is_logged_out(self, client):
        response = client.get(reverse("profile_delete"))
        assert response.status_code == 302
        assertRedirects(
            response, "/accounts/login/?next=/accounts/profile/delete/"
        )

    def test_view_deletes_user_account_after_getting_of_form_data(
        self, client, create_logged_in_user
    ):
        response = client.post(reverse("profile_delete"))
        assert response.status_code == 302
        assertRedirects(response, reverse("cinema:index"))
        assert User.objects.count() == 0

        redirect_url = response.url
        next_response = client.get(redirect_url)

        assert next_response.status_code == 200
        assert next_response.context["user"].is_anonymous

        for message in next_response.context["messages"]:
            if message.tags == "success":
                assert message.message == "User account has been deleted."


@pytest.mark.django_db
class TestUserPasswordResetView:
    def test_view_url_exists_at_desired_location(
        self, client, create_activated_user
    ):
        response = client.get("/accounts/password/reset/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_activated_user):
        response = client.get(reverse("password_reset"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_activated_user):
        response = client.get(reverse("password_reset"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/password_reset.html")

    def test_view_redirects_to_password_reset_done_url_after_getting_form_data(
        self, client, create_activated_user
    ):
        response = client.post(
            path=reverse("password_reset"),
            data={"email": "test.username@example.com"},
        )
        assert response.status_code == 302
        assertRedirects(response, reverse("password_reset_done"))


@pytest.mark.django_db
class TestUserPasswordResetDoneView:
    def test_view_url_exists_at_desired_location(self, client):
        response = client.get("/accounts/password/reset/done/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client):
        response = client.get(reverse("password_reset_done"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client):
        response = client.get(reverse("password_reset_done"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/reset_done.html")


@pytest.mark.django_db
class TestUserPasswordResetCompleteView:
    def test_view_url_exists_at_desired_location(self, client):
        response = client.get("/accounts/password/confirm/complete/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client):
        response = client.get(reverse("password_reset_complete"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client):
        response = client.get(reverse("password_reset_complete"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/password_complete.html")

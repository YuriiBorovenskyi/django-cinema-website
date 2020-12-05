import pytest
from django.contrib.auth.password_validation import (
    password_validators_help_text_html,
)
from django.core.exceptions import ValidationError
from django.forms import PasswordInput

from accounts.forms import (
    ChangeUserInfoForm,
    RegisterUserForm,
)
from accounts.models import User


class TestChangeUserInfoForm:
    def test_form_is_created_from_model(self):
        form = ChangeUserInfoForm()
        assert form.Meta.model is User

    def test_model_fields_is_included_to_form(self):
        form = ChangeUserInfoForm()

        for field in ("username", "email", "first_name", "last_name"):
            assert field in form.Meta.fields

    def test_email_field_label_of_form(self):
        form = ChangeUserInfoForm()

        assert (
            form.fields["email"].label is None
            or form.fields["email"].label == "E-mail"
        )

    def test_email_field_options_of_form(self):
        form = ChangeUserInfoForm()
        assert form.fields["email"].required


class TestRegisterUserForm:
    label_arg_values = (
        ("email", "E-mail"),
        ("password1", "Password"),
        ("password2", "Password (again)"),
    )
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("email", "required", True),
        ("password1", "widget", PasswordInput),
        ("password1", "help_text", password_validators_help_text_html()),
        ("password2", "widget", PasswordInput),
        (
            "password2",
            "help_text",
            "Enter the same password again for " "verification",
        ),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_form_is_created_from_model(self):
        form = RegisterUserForm()
        assert form.Meta.model is User

    def test_model_fields_is_included_to_form(self):
        form = RegisterUserForm()

        for field in (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        ):
            assert field in form.Meta.fields

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_form_fields(self, field_name, expected_label):
        form = RegisterUserForm()
        actual_label = form.fields[field_name].label

        assert (
            actual_label is None
            or form.fields[field_name].label == expected_label
        )

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_form_fields(
        self,
        field_name,
        option_name,
        expected_option_value,
    ):
        form = RegisterUserForm()

        if option_name == "required":
            actual_option_value = form.fields[field_name].required
            assert actual_option_value == expected_option_value
        elif option_name == "widget":
            actual_option_value = form.fields[field_name].widget
            assert isinstance(actual_option_value, expected_option_value)
        else:
            actual_option_value = form.fields[field_name].help_text
            assert actual_option_value == expected_option_value

    @pytest.mark.django_db
    def test_validation_form_with_correct_data(self):
        form_data = {
            "username": "ivan.ivanov",
            "email": "ivan.ivanov@example.com",
            "password1": "ivan_password",
            "password2": "ivan_password",
            "first_name": "Ivan",
            "last_name": "Ivanov",
        }
        form = RegisterUserForm(data=form_data)

        assert form.is_valid()
        assert form.clean_password1() == "ivan_password"
        assert form.clean_password2() == "ivan_password"
        assert not form.clean()

    @pytest.mark.django_db
    def test_validation_form_with_incorrect_data(self):
        form_data = {
            "username": "ivan.ivanov",
            "email": "ivan.ivanov@example.com",
            "password1": "ivan_password_1",
            "password2": "ivan_password_2",
            "first_name": "Ivan",
            "last_name": "Ivanov",
        }
        form = RegisterUserForm(data=form_data)

        assert not form.is_valid()

        with pytest.raises(ValidationError) as exc_info:
            form.clean()
        assert (
            str(exc_info.value)
            == "{'password2': ['The passwords entered do not match']}"
        )

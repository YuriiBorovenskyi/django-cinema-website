import pytest

from django.contrib.auth.models import AbstractUser

from accounts.models import User

user_emails = [
    "ivan.ivanov@example.com",
    "petr.petrov@example.com",
    "fyodor.fyodorov@example.com"
]


@pytest.mark.django_db
class TestUserModel:
    label_argvalues = [("email", "Email address"), ]
    label_ids = [
        f"'{arg[0]}' field: is label '{arg[1]}'?"
        for arg in label_argvalues
    ]
    field_argvalues = [
        ("email", "unique", True),
    ]
    field_ids = [
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?"
        for arg in field_argvalues
    ]

    def test_user_model_is_chield_of_abstract_user_model(self):
        assert issubclass(User, AbstractUser)

    def test_record_is_instance_of_model(self, user):
        assert isinstance(user, User)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_argvalues,
        ids=label_ids
    )
    def test_label_of_model_field(
            self, user, field_name, expected_label
    ):
        actual_label = user._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_argvalues,
        ids=field_ids
    )
    def test_options_of_model_fields(
            self, user, field_name, option_name, expected_option_value
    ):
        if option_name == "unique":
            actual_option_value = user._meta.get_field(field_name).unique
        else:
            raise AttributeError(
                f"String '{option_name}' cannot be an attribute."
            )
        assert actual_option_value == expected_option_value

    def test_values_of_record_fields(self, user_factory):
        user = user_factory(email=user_emails[0])
        actual_email = user.email
        expected_email = user_emails[0]
        assert actual_email, expected_email
        assert User.objects.count() == 1

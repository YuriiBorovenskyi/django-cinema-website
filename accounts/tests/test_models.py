import pytest
from django.contrib.auth.models import AbstractUser

from accounts.models import User


@pytest.mark.django_db
class TestUserModel:
    def test_user_model_is_child_of_abstract_user_model(self):
        assert issubclass(User, AbstractUser)

    def test_record_is_instance_of_model_class(self, user):
        assert isinstance(user, User)

    def test_email_field_label_of_model(self, user):
        assert user._meta.get_field("email").verbose_name == "Email address"

    def test_email_field_options_of_model(self, user):
        assert user._meta.get_field("email").unique

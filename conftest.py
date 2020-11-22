import pytest
from django.db.models.signals import post_save
from pytest_factoryboy import register

from accounts.models import user_registrated
from accounts.tests.factories import UserFactory

register(UserFactory)


@pytest.fixture(autouse=True)
def mute_signals(request):
    post_save.receivers = []
    user_registrated.receivers = []


@pytest.fixture
def create_non_activated_user(db):
    user = UserFactory.create(
        username="test.username",
        first_name="test_first_name",
        last_name="test_last_name",
    )
    user.set_password("test_password")
    user.is_active = False
    user.save()


@pytest.fixture
def create_activated_user(db):
    user = UserFactory.create(
        username="test.username",
        first_name="test_first_name",
        last_name="test_last_name",
    )
    user.set_password("test_password")
    user.save()


@pytest.fixture
def create_logged_in_user(db, client):
    user = UserFactory.create(
        username="test.username",
        first_name="test_first_name",
        last_name="test_last_name",
    )
    user.set_password("test_password")
    user.save()
    client.login(username="test.username", password="test_password")

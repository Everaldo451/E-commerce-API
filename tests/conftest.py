from django.test import Client
import pytest
from django.core.management import call_command


@pytest.fixture(scope="session")
def apply_migrations(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("migrate")

@pytest.fixture
def client():
    return Client()
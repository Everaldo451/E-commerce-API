from src.backend.core.validators.password import messages

import pytest
import logging

@pytest.mark.django_db
class TestCreate:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.url = '/api/v1/users/'
        self.data = {
            'username': 'Username',
            'email': 'user@example.com',
            'first_name': 'AnyName',
            'last_name': 'AnyLastName',
            'password': 'valid123Password$',
        }

    @pytest.fixture
    def create_user(self, django_user_model):
        django_user_model.objects.create_user(**self.data)

    def test_success(self, client):
        response = client.post(
            self.url,
            data=self.data
        )

        assert response.status_code == 201
        json = response.json()
        assert isinstance(json, dict)

        assert json.get('id') is not None
        assert json.get('username') == self.data.get('username')
        assert json.get('email') == self.data.get('email')
        assert json.get('first_name') == self.data.get('first_name')
        assert json.get('last_name') == self.data.get('last_name')
        assert json.get('is_staff') == False

    def test_user_already_exists(self, client, create_user):
        response = client.post(
            self.url,
            data=self.data
        )

        assert response.status_code == 400
        json = response.json()
        assert json.get('username') is not None
        assert json.get('email') is not None

    def test_invalid_data(self, client):
        response = client.post(
            self.url,
            data={
                **self.data, 
                'email': 'invalidemail', 
                'password': 'invalid'
            }
        )

        assert response.status_code == 400
        json = response.json()
        assert isinstance(json, dict)

        assert json.get('email') is not None
        assert json.get('password') is not None
        
        password = json.get('password')
        for value in messages.values():
            assert value in password



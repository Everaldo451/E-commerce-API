import pytest

@pytest.mark.django_db
class TestLogout:

    @pytest.fixture(autouse=True)
    def setup(self, django_user_model, client):
        self.url = '/api/v1/auth/logout/'
        user_data = {
            'username': 'Username',
            'email': 'user@example.com',
            'password': 'password',
            'first_name': 'AnyName',
            'last_name': 'AnyLastName'
        }
        django_user_model.objects.create_user(**user_data)
        response = client.post(
            '/api/v1/auth/login/',
            data=user_data
        )

        tokens = response.json().get('tokens')
        refresh_token_value = tokens.get('refresh_token').get('value')
        self.data = {
            'refresh': refresh_token_value
        }

    def test_success(self, client):
        response = client.post(
            self.url,
            data=self.data,
        )

        assert response.status_code==200
        json = response.json()
        assert json is not None

    def test_unauthorized(self, client):
        response = client.post(
            self.url,
            data={
                'refresh': 'Bearer invalidtoken'
            }
        )

        assert response.status_code==401
        json = response.json()
        assert json is not None

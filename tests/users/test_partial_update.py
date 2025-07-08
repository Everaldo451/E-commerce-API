from rest_framework_simplejwt.tokens import AccessToken
import pytest

@pytest.mark.django_db
class TestUpdate:

    @pytest.fixture(autouse=True)
    def setup(self, django_user_model):
        user_data = {
            'username': 'Username',
            'email': 'user@example.com',
            'first_name': 'AnyName',
            'last_name': 'AnyLastName',
            'password': 'valid123Password$',
        }
        user = django_user_model.objects.create_user(**user_data)
        self.url = f'/api/v1/users/{user.id}/'
        
        access_token = str(AccessToken.for_user(user))
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }
        self.data = {
            'username': 'AnotherUsername'
        }

    def test_success(self, client):
        response = client.patch(
            self.url,
            data=self.data,
            headers=self.headers,
            content_type='application/json'
        )

        assert response.status_code == 200
        json = response.json()
        assert json is not None
        assert json.get('username') == self.data.get('username')

    def test_unauthorized(self, client):
        response = client.patch(
            self.url,
            data=self.data,
            headers={
                'Authorization': 'Bearer invalidtoken'
            },
            content_type='application/json'
        )

        assert response.status_code == 401

    def test_invalid_data(self, client):
        response = client.patch(
            self.url,
            data={
                'email': 'invalidemail',
                'password': 'invalid_password'
            },
            headers=self.headers,
            content_type='application/json'
        )

        assert response.status_code == 400
        json = response.json()
        assert json is not None
        assert json.get('email') is not None
        assert json.get('password') is not None
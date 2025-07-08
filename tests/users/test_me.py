from rest_framework_simplejwt.tokens import AccessToken
import pytest

@pytest.mark.django_db
class TestMe:

    @pytest.fixture(autouse=True)
    def setup(self, django_user_model):
        user_data = {
            'username': 'Username',
            'email': 'user@example.com',
            'first_name': 'AnyName',
            'last_name': 'AnyLastName',
            'password': 'valid123Password$',
        }
        self.user = django_user_model.objects.create_user(**user_data)
        self.url = f'/api/v1/users/me/'
        
        access_token = str(AccessToken.for_user(self.user))
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    def test_success(self, client):
        response = client.get(
            self.url,
            headers=self.headers,
        )
        assert response.status_code == 200
        json = response.json()
        assert json.get('id') == str(self.user.id)
        assert json.get('username') == self.user.username
        assert json.get('email') == self.user.email
        assert json.get('first_name') == self.user.first_name
        assert json.get('last_name') == self.user.last_name
        assert json.get('is_staff') == self.user.is_staff
        assert json.get('password') is None

    def test_unauthorized(self, client):
        response = client.get(
            self.url,
            headers={
                'Authorization': 'Bearer invalidtoken'
            },
        )
        assert response.status_code == 401
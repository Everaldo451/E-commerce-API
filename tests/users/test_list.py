from rest_framework_simplejwt.tokens import AccessToken
import pytest

@pytest.mark.django_db
class TestList:

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
        self.url = f'/api/v1/users/'
        
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
        assert len(json) == 1
        user = json[0]
        assert user.get('id') == str(self.user.id)
        assert user.get('username') == self.user.username
        assert user.get('email') == self.user.email
        assert user.get('first_name') == self.user.first_name
        assert user.get('last_name') == self.user.last_name
        assert user.get('is_staff') == self.user.is_staff
        assert user.get('password') is None

    def test_unauthorized(self, client):
        response = client.get(
            self.url,
            headers={
                'Authorization': 'Bearer invalidtoken'
            },
        )

        assert response.status_code == 401
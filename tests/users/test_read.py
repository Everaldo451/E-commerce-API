from rest_framework_simplejwt.tokens import AccessToken
import pytest

@pytest.mark.django_db
class TestRead:

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
        self.url = f'/api/v1/users/{self.user.id}/'
        
        access_token = str(AccessToken.for_user(self.user))
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }
        self.data = {
            'username': 'AnotherUsername'
        }

    def test_success(self, client):
        response = client.get(
            self.url,
            headers=self.headers
        )

        assert response.status_code == 200
        json = response.json()
        assert json is not None

    def test_unauthorized(self, client):
        response = client.get(
            self.url,
            headers={
                'Authorization': 'Bearer invalidtoken'
            },
            content_type='application/json'
        )

        assert response.status_code == 401
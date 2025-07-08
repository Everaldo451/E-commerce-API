from rest_framework_simplejwt.tokens import AccessToken
import pytest

@pytest.mark.django_db
class TestDelete:

    @pytest.fixture(autouse=True)
    def setup(self, django_user_model, client):
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

    def test_success(self, client):
        response = client.delete(
            self.url,
            headers=self.headers,
            content_type='application/json'
        )
        assert response.status_code == 204

    def test_unauthorized(self, client):
        response = client.patch(
            self.url,
            headers={
                'Authorization': 'Bearer invalidtoken'
            },
            content_type='application/json'
        )

        assert response.status_code == 401
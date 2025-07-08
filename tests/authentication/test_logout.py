from rest_framework_simplejwt.tokens import RefreshToken
import pytest

@pytest.mark.django_db
class TestLogout:

    @pytest.fixture(autouse=True)
    def setup(self, django_user_model):
        self.url = '/api/v1/auth/logout/'
        user_data = {
            'username': 'Username',
            'email': 'user@example.com',
            'first_name': 'AnyName',
            'last_name': 'AnyLastName',
            'password': 'valid123Password$',
        }
        user = django_user_model.objects.create_user(**user_data)
        
        refresh_token = str(RefreshToken.for_user(user))
        self.data = {
            'refresh': refresh_token
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

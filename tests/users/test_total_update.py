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
            'username': 'AnotherUsername',
            'email': 'anotheruser@example.com',
            'first_name': 'AnotherName',
            'last_name': 'AnotherLastName',
            'password': 'othervalid123Password$'
        }

    def test_success(self, client):
        response = client.put(
            self.url,
            data=self.data,
            headers=self.headers,
            content_type='application/json'
        )

        assert response.status_code == 200
        json = response.json()
        assert json is not None
        assert json.get('username') == self.data.get('username')
        assert json.get('email') == self.data.get('email')
        assert json.get('first_name') == self.data.get('first_name')
        assert json.get('last_name') == self.data.get('last_name')
        assert json.get('password') is None

    def test_unauthorized(self, client):
        response = client.put(
            self.url,
            data=self.data,
            headers={
                'Authorization': 'Bearer invalidtoken'
            },
            content_type='application/json'
        )

        assert response.status_code == 401

    def test_incomplete_data(self, client):
        response = client.put(
            self.url,
            data={
                'username': self.data.get('username')
            },
            headers=self.headers,
            content_type='application/json'
        )

        assert response.status_code == 400
        json = response.json()
        assert json is not None
import pytest

@pytest.mark.django_db
class TestLogin:

    @pytest.fixture(autouse=True)
    def setup(self, django_user_model):
        self.url = '/api/v1/auth/login/'
        self.user_data = {
            'username': 'Username',
            'email': 'user@example.com',
            'first_name': 'AnyName',
            'last_name': 'AnyLastName',
            'password': 'valid123Password$',
        }
        self.data = {
            'email': self.user_data.get('email'),
            'password': self.user_data.get('password')
        }
        django_user_model.objects.create_user(**self.user_data)

    def test_success(self, client):
        response = client.post(
            self.url,
            data=self.data
        )

        assert response.status_code==201
        json = response.json()
        assert json is not None

        user = json.get('user')
        assert isinstance(user, dict)
        assert user.get('id') is not None
        assert user.get('username') == self.user_data.get('username')
        assert user.get('email') == self.user_data.get('email')
        assert user.get('first_name') == self.user_data.get('first_name')
        assert user.get('last_name') == self.user_data.get('last_name')
        assert user.get('is_staff') == False

        tokens = json.get('tokens')
        assert isinstance(tokens, dict)

    def test_invalid_user_data(self, client):
        response = client.post(
            self.url,
            data={
                **self.data,
                'password': 'anotherpassword'
            }
        )

        assert response.status_code==400
        json = response.json()
        assert json is not None
        non_field_errors = json.get('non_field_errors')
        assert non_field_errors is not None

    def test_readonly_fields(self, client):
        response = client.post(
            self.url,
            data={
                **self.data,
                'is_staff': True,
            }
        )

        assert response.status_code==201
        json = response.json()
        assert json is not None

        user = json.get('user')
        assert user.get('is_staff')==False

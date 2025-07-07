import pytest

@pytest.mark.django_db
class TestLogin:

    @pytest.fixture(autouse=True)
    def setup(self, django_user_model):
        self.url = '/api/v1/auth/login/'
        self.user_data = {
            'username': 'Username',
            'email': 'user@example.com',
            'password': 'password',
            'first_name': 'AnyName',
            'last_name': 'AnyLastName'
        }
        django_user_model.objects.create_user(**self.user_data)

    def test_success(self, client):
        response = client.post(
            self.url,
            data=self.user_data
        )

        assert response.status_code==201
        json = response.json()
        assert json is not None

        user = json.get('user')
        assert isinstance(user, dict)
        for key, value in user.items():
            user_data_value = self.user_data.get(key)
            if self.user_data.get(key) is None:
                continue
            assert user_data_value == value

        tokens = json.get('tokens')
        assert isinstance(tokens, dict)

    def test_invalid_user_data(self, client):
        response = client.post(
            self.url,
            data={
                **self.user_data,
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
                **self.user_data,
                'is_staff': True,
            }
        )

        assert response.status_code==201
        json = response.json()
        assert json is not None

        user = json.get('user')
        assert user.get('is_staff')==False

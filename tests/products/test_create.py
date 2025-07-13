from rest_framework_simplejwt.tokens import AccessToken
import pytest
import logging

@pytest.mark.django_db
class TestCreate:

    @pytest.fixture(autouse=True)
    def setup(self, django_user_model):
        user_data = {
            'username': 'Username',
            'email': 'user@example.com',
            'password': 'valid@Password123',
            'first_name': 'Name',
            'last_name': 'Last Name'
        }
        user = django_user_model.objects.create_user(**user_data)
        access_token = str(AccessToken.for_user(user))

        self.url = '/api/v1/products/'
        self.data = {
            'name': 'Product',
            'price': '10.0',
            'stock': 100,
            'tags': [
                {
                    'name': 'tag1'
                },
                {
                    'name':'tag2'
                }
            ],
            'media': []
        }
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }
    
    @pytest.fixture
    def create_tags(self):
        from products.models import Tag
        for tag in self.data['tags']:
            Tag.objects.create(**tag)
    
    def test_success(self, client):
        logging.debug('Start create product test')
        response = client.post(
            self.url,
            data=self.data,
            headers=self.headers,
            content_type='application/json'
        )

        assert response.status_code==201, f'Erro: {response.status_code} - {response.json()}'
        json = response.json()
        assert json is not None

    def test_unauthorized(self, client):
        logging.debug('Start create product with anonymous user test')
        response = client.post(
            self.url,
            data=self.data,
            content_type='application/json'
        )

        assert response.status_code==401

    def test_tags_already_exists(self, client, create_tags):
        logging.debug('Start create product with tags that already exists test')
        response = client.post(
            self.url,
            data=self.data,
            headers=self.headers,
            content_type='application/json'
        )

        assert response.status_code==201, f'Erro: {response.status_code} - {response.json()}'
        json = response.json()
        assert json is not None


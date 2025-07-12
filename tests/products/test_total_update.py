from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken
import pytest

@pytest.mark.django_db
class TestTotalUpdate:

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

        product_data = {
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

        factory = APIRequestFactory()
        request = factory.post('/api/v1/products/', data=product_data, format='json')
        request.user = user

        from products.serializer import ProductSerializer
        serializer = ProductSerializer(data=product_data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        post = serializer.save()

        self.url = f'/api/v1/products/{post.id}/'
        self.data = {
            'name': 'Product2',
            'price': '20.0',
            'stock': 200,
            'tags': [
                {
                    'name': 'tag3'
                },
            ],
            'media': []
        }
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }
    
    def test_success(self, client):
        response = client.put(
            self.url,
            data=self.data,
            headers=self.headers,
            content_type='application/json'
        )

        assert response.status_code==200

    def test_unauthorized(self, client):
        response = client.put(
            self.url,
            data=self.data,
            content_type='application/json'
        )

        assert response.status_code==401

    def test_incomplete_data(self, client):
        data = {**self.data,}
        data.pop('name')

        response = client.put(
            self.url,
            data=data,
            headers=self.headers,
            content_type='application/json'
        )

        assert response.status_code==400
        json = response.json()
        assert json is not None
        assert json.get('name') is not None


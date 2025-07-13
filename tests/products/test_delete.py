from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken
import pytest
import logging

@pytest.mark.django_db
class TestDelete:

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
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }
    
    def test_success(self, client):
        logging.debug('Start delete product test')
        response = client.delete(
            self.url,
            headers=self.headers,
            content_type='application/json'
        )

        assert response.status_code==204

    def test_unauthorized(self, client):
        logging.debug('Start delete product with anonymous user test')
        response = client.delete(
            self.url,
            content_type='application/json'
        )

        assert response.status_code==401


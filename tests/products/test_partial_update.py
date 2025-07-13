from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken
import pytest
import logging

@pytest.mark.django_db
class TestPartialUpdate:

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
            'price': '20.00',
            'tags': [
                {
                    'name': 'tag3'
                },
            ],
        }
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }
    
    def test_success(self, client):
        logging.debug('Start partial update test')
        response = client.patch(
            self.url,
            data=self.data,
            headers=self.headers,
            content_type='application/json'
        )

        assert response.status_code==200, f'Erro: {response.status_code} - {response.json()}'
        json = response.json()
        assert json.get('name') == self.data['name']
        assert json.get('price') == self.data['price']

        tags = json.get('tags')
        copy_tags = [
            {'name':  tag['name']} for tag in tags
        ]
        for tag in self.data['tags']:
            assert tag in copy_tags

    def test_unauthorized(self, client):
        logging.debug('Start partial update with anonymous user test')
        response = client.patch(
            self.url,
            data=self.data,
            content_type='application/json'
        )

        assert response.status_code==401

    def test_tag_already_exists(self, client):
        logging.debug('Start partial update with tags that already exists test')
        response = client.patch(
            self.url,
            data={
                **self.data,
                'tags': [
                    {
                        'name': 'tag1'
                    }
                ]
            },
            headers=self.headers,
            content_type='application/json'
        )

        assert response.status_code==200, f'Erro: {response.status_code} - {response.json()}'
        json = response.json()
        assert json is not None



from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken
import pytest

@pytest.mark.django_db
class TestRead:

    @pytest.fixture(autouse=True)
    def setup(self, django_user_model):
        user_data = {
            'username': 'Username',
            'email': 'user@example.com',
            'password': 'valid@Password123',
            'first_name': 'Name',
            'last_name': 'Last Name'
        }
        other_user_data = {
            'username': 'Otherusername',
            'email': 'other@example.com',
            'password': 'valid@Password123',
            'first_name': 'Name',
            'last_name': 'Last Name'
        }
        user = django_user_model.objects.create_user(**user_data)
        access_token = str(AccessToken.for_user(user))

        other_user = django_user_model.objects.create_user(**other_user_data)
        self.other_user_access_token = str(AccessToken.for_user(other_user))

        self.data = {
            'name': 'Product',
            'price': '10.00',
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
        request = factory.post('/api/v1/products/', data=self.data, format='json')
        request.user = user

        from products.serializer import ProductSerializer
        serializer = ProductSerializer(data=self.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        post = serializer.save()

        self.url = f'/api/v1/products/{post.id}/'
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }
    
    def test_is_anonymous_user(self, client):
        response = client.get(
            self.url,
            content_type='application/json'
        )

        assert response.status_code==200
        json = response.json()
        assert json.get('name') == self.data['name']
        assert json.get('price') == self.data['price']

        tags = json.get('tags')
        copy_tags = [
            {'name':  tag['name']} for tag in tags
        ]
        for tag in self.data['tags']:
            assert tag in copy_tags

    def test_is_owner_user(self, client):
        response = client.get(
            self.url,
            headers=self.headers,
            content_type='application/json'
        )

        assert response.status_code==200
        json = response.json()
        assert json.get('name') == self.data['name']
        assert json.get('price') == self.data['price']

        tags = json.get('tags')
        copy_tags = [
            {'name':  tag['name']} for tag in tags
        ]
        for tag in self.data['tags']:
            assert tag in copy_tags

    def test_is_authenticated_user(self, client):
        response = client.get(
            self.url,
            headers={
                'Authorization': self.other_user_access_token
            },
            content_type='application/json'
        )

        assert response.status_code==200
        json = response.json()
        assert json.get('name') == self.data['name']
        assert json.get('price') == self.data['price']

        tags = json.get('tags')
        copy_tags = [
            {'name':  tag['name']} for tag in tags
        ]
        for tag in self.data['tags']:
            assert tag in copy_tags



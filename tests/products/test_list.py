from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken
import pytest

@pytest.mark.django_db
class TestList:

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

        self.data = [
            {
                'name': f'Product{i}',
                'price': f'{1*i}0.00',
                'stock': f'{1*i}0.00',
                'tags': [
                    {
                        'name': f'tag{i}'
                    }
                ],
                'media': []
            } for i in range(1,4)
        ]

        factory = APIRequestFactory()
        request = factory.post('/api/v1/products/', data=self.data, format='json')
        request.user = user

        from products.serializer import ProductSerializer
        for product in self.data:
            serializer = ProductSerializer(data=product, context={'request':request})
            serializer.is_valid(raise_exception=True)
            post = serializer.save()

        self.url = f'/api/v1/products/'
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
        for idx, product in enumerate(json):
            current_product = self.data[idx]
            assert product.get('name') == current_product['name']
            assert product.get('price') == current_product['price']

            tags = product.get('tags')
            copy_tags = [
                {'name':  tag['name']} for tag in tags
            ]
            for tag in current_product['tags']:
                assert tag in copy_tags

    def test_is_owner_user(self, client):
        response = client.get(
            self.url,
            headers=self.headers,
            content_type='application/json'
        )

        assert response.status_code==200
        json = response.json()
        for idx, product in enumerate(json):
            current_product = self.data[idx]
            assert product.get('name') == current_product['name']
            assert product.get('price') == current_product['price']

            tags = product.get('tags')
            copy_tags = [
                {'name':  tag['name']} for tag in tags
            ]
            for tag in current_product['tags']:
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
        for idx, product in enumerate(json):
            current_product = self.data[idx]
            assert product.get('name') == current_product['name']
            assert product.get('price') == current_product['price']

            tags = product.get('tags')
            copy_tags = [
                {'name':  tag['name']} for tag in tags
            ]
            for tag in current_product['tags']:
                assert tag in copy_tags



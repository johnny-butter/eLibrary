from rest_framework.test import APITestCase
from api import factory


class ApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = factory.UserFactory.create()
        factory.BookFactory.create()

    def test_create_user(self):
        user_data = {
            'username': 'test2',
            'password': 'test2',
            'email': 'test2@test.com',
        }

        response = self.client.post('/api/v2/user/', data=user_data)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data.get(
            'username', None), 'test2', response.data)
        self.assertEqual(response.data.get(
            'email', None), 'test2@test.com', response.data)

        self.assertFalse(response.data.get('password', False), response.data)
        self.assertFalse(response.data.get('is_staff', None), response.data)
        self.assertFalse(response.data.get(
            'is_superuser', None), response.data)

    def test_get_user_without_jwt(self):
        response = self.client.get('/api/v2/user/')

        self.assertEqual(
            response.data['detail']['code'], 'not_authenticated', response.data)

    def test_get_user_with_jwt(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v2/user/')

        self.assertEqual(response.data.get('id', None), 1, response.data)
        self.assertEqual(response.data.get('username', None), 'test_user')
        self.assertEqual(response.data.get('password', None), None)
        self.assertEqual(response.data.get('email', None), 'test@test.com')

    def test_modify_user(self):
        data = {
            'username': 'testtest',
            'email': 'testtest@test.com',
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.put('/api/v2/user/', data=data, format='json')

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data.get(
            'username', None), 'testtest', response.data)
        self.assertFalse(response.data.get('password', False), response.data)
        self.assertEqual(response.data.get(
            'email', None), 'testtest@test.com', response.data)

        self.assertFalse(response.data.get('is_staff', None), response.data)
        self.assertFalse(response.data.get(
            'is_superuser', None), response.data)

    def test_get_book_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v2/get_all_book/')

        self.assertEqual(response.data['total_page'], 1, response.data)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['name'], 'test_book')
        self.assertEqual(response.data['data'][0]['type_name'], 'test')
        self.assertEqual(response.data['data'][0]['price_discount'], 50)

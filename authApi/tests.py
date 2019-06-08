import json
from rest_framework.test import APITestCase
# from rest_framework.test import APIRequestFactory
# from rest_framework.test import RequestsClient
from django.urls import reverse
from .models import User, Book, bookType


class apiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # super(apiTests, cls).setUpClass()
        User.objects.create_user(id=1, username='test', password='test',
                                 email='test@test.com')
        cls.user = User.objects.get(username='test')
        b = bookType.objects.create(name='travel')
        Book.objects.create(name='test book', type=b, publish_date='2019-04-03',
                            price_origin='200', price_discount='100')

    def test_get_token_wrong_info(self):
        response = self.client.post(
            '/api/token/',
            data={'username': 'test', 'password': 'testWrong'})

        self.assertEqual(response.data.get('non_field_errors', None)[0],
                         'No active account found with the given credentials', response.data)

    def test_get_token_by_username(self):
        response = self.client.post(
            '/api/token/',
            data={'username': 'test', 'password': 'test'})

        self.assertEqual(response.status_code, 200, response.data)
        self.assertTrue(response.data.get('access', None), response.data)
        self.assertTrue(response.data.get('refresh', None), response.data)

    def test_get_token_by_email(self):
        response = self.client.post(
            '/api/token/', data={'username': 'test@test.com', 'password': 'test'})

        self.assertEqual(response.status_code, 200, response.data)
        self.assertTrue(response.data.get('access', None), response.data)
        self.assertTrue(response.data.get('refresh', None), response.data)

    def test_cbv_create_user(self):
        response = self.client.post(
            '/api/cbv/user/',
            data={'username': 'test2', 'password': 'test2', 'email': 'test2@test.com'})

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data.get(
            'username', None), 'test2', response.data)
        self.assertFalse(response.data.get('password', False), response.data)
        self.assertEqual(response.data.get('email', None),
                         'test2@test.com', response.data)
        self.assertFalse(response.data.get('is_staff', None), response.data)
        self.assertFalse(response.data.get(
            'is_superuser', None), response.data)

    def test_cbv_get_user_none_token(self):
        response = self.client.get('/api/cbv/user/1/')

        self.assertEqual(response.data.get('detail', None),
                         'This is not you', response.data)

    def test_cbv_get_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/cbv/user/1/')

        self.assertEqual(response.data.get('id', None), 1, response.data)
        self.assertEqual(response.data.get('username', None), 'test')
        self.assertEqual(response.data.get('password', None), None)
        self.assertEqual(response.data.get('email', None), 'test@test.com')

    def test_cbv_modify_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/api/cbv/user/1/',
                                   data={'username': 'testtest',
                                         'email': 'testtest@test.com'},
                                   format='json')

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data.get(
            'username', None), 'testtest', response.data)
        self.assertFalse(response.data.get('password', False), response.data)
        self.assertEqual(response.data.get('email', None),
                         'testtest@test.com', response.data)
        self.assertFalse(response.data.get('is_staff', None), response.data)
        self.assertFalse(response.data.get(
            'is_superuser', None), response.data)

    def test_cbv_get_book_list(self):
        response = self.client.get('/api/cbv/getallbook/')

        data = json.loads(response.content)

        self.assertEqual(data['total_page'], 1, data)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['name'], 'test book')
        self.assertEqual(data['data'][0]['type_name'], 'travel')
        self.assertEqual(data['data'][0]['price_discount'], 100)

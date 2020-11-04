from rest_framework.test import APITestCase, APITransactionTestCase

from django.test import override_settings

from api import factory
from multiprocessing.pool import ThreadPool as Pool


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

        response = self.client.post('/en/api/v2/user/', data=user_data)

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
        response = self.client.get('/en/api/v2/user/')

        self.assertEqual(
            response.data['detail']['code'], 'not_authenticated', response.data)

    def test_get_user_with_jwt(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/en/api/v2/user/')

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
        response = self.client.put('/en/api/v2/user/', data=data, format='json')

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
        response = self.client.get('/en/api/v2/get_all_book/')

        self.assertEqual(response.data['total_page'], 1, response.data)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['name'], 'test_book')
        self.assertEqual(response.data['data'][0]['type_name'], 'test')
        self.assertEqual(response.data['data'][0]['price_discount'], 50)


@override_settings(CACHES={'default': {
    'BACKEND': 'django_redis.cache.RedisCache',
    'LOCATION': 'redis://172.30.137.182:6379/3'
}})
class BookStockTest(APITransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(BookStockTest, cls).setUpClass()
        cls.user = factory.UserFactory.create()

    def test_concurrent_add_cart(self):
        CONCURRENT = 5
        book = factory.BookFactory.create(stock=CONCURRENT)

        def add_book_to_cart(book_id):
            self.client.force_authenticate(user=self.user)
            resp = self.client.post('/en/api/v2/cart/?action=add', data={'book': book_id})
            return resp

        pool = Pool(CONCURRENT)
        for _ in range(CONCURRENT):
            pool.apply_async(add_book_to_cart, args=(book.id,))

        pool.close()
        pool.join()
        book.refresh_from_db()

        self.assertEqual(book.stock, 0)

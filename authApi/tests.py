from rest_framework.test import APITestCase
# from rest_framework.test import APIRequestFactory
# from rest_framework.test import RequestsClient
from django.urls import reverse
from .models import Book, bookType


class bookTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super(bookTests, cls).setUpClass()
        b = bookType.objects.create(name='travel')
        Book.objects.create(name='test book', type=b, publish_date='2019-04-03',
                            price_origin='200', price_discount='100')

    def test_get_book_list(self):
        response = self.client.get('/api/cbv/getallbook/')

        self.assertEqual(response.data['total_page'], 1)
        self.assertEqual(len(response.data['data']), 1, response.data['data'])
        self.assertEqual(response.data['data'][0]['name'], 'test book')
        self.assertEqual(response.data['data'][0]['type_name'], 'travel')
        self.assertEqual(response.data['data'][0]['price_discount'], 100)

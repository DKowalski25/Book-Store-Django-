from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1')
        book2 = Book.objects.create(name='Test book 2', price=55, author_name='Author 2')
        data = BooksSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Author 1',
                'owner': None,
                'readers': []
            },
            {
                'id': book2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'author_name': 'Author 2',
                'owner': None,
                'readers': []

            }
        ]
        actual_data = [dict(item) for item in data]
        self.assertEqual(expected_data, actual_data)

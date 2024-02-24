from django.contrib.auth.models import User
from django.test import TestCase


from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user 1')
        user2 = User.objects.create(username='user 2')
        user3 = User.objects.create(username='user 3')
        book1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1')
        book2 = Book.objects.create(name='Test book 2', price=55, author_name='Author 2')

        UserBookRelation.objects.create(user=user1, book=book1, like=True)
        UserBookRelation.objects.create(user=user2, book=book1, like=True)
        UserBookRelation.objects.create(user=user3, book=book1, like=True)

        UserBookRelation.objects.create(user=user1, book=book2, like=True)
        UserBookRelation.objects.create(user=user2, book=book2, like=True)
        UserBookRelation.objects.create(user=user3, book=book2, like=False)

        data = BooksSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Author 1',
                # 'owner': None,
                # 'readers': []
                'likes_count': 3
            },
            {
                'id': book2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'author_name': 'Author 2',
                # 'owner': None,
                # 'readers': []
                'likes_count': 2

            }
        ]
        actual_data = [dict(item) for item in data]
        self.assertEqual(expected_data, actual_data)

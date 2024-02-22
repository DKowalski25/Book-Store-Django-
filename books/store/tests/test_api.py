import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='Test_user')
        self.book1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1')
        self.book2 = Book.objects.create(name='Test book 2', price=55, author_name='Author 3')
        self.book3 = Book.objects.create(name='Test book 3 Author 1', price=55, author_name='Author 2')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer([self.book1, self.book2, self.book3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_one(self):
        url = reverse('book-detail', args=(self.book1.id,))
        response = self.client.get(url)
        serializer_data = BooksSerializer(self.book1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BooksSerializer([self.book1, self.book3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 55})
        serializer_data = BooksSerializer([self.book2, self.book3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_order(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price'})
        serializer_data = BooksSerializer([self.book1, self.book2, self.book3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            'name': 'Book 1',
            'price': 250,
            'author_name': 'Author 1'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())

    def test_update(self):
        url = reverse('book-detail', args=(self.book1.id,))
        data = {
            'name': self.book1.name,
            'price': 250,
            'author_name': self.book1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(250, self.book1.price)

    def test_delete(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())


from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from library.models import Reader, Book


class LibraryTest(APITestCase):

    def setUp(self) -> None:
        self.reader_1 = Reader.objects.create(first_name="Petr1", last_name="Petrov1", passport_number="1100998877")
        self.reader_2 = Reader.objects.create(first_name="Petr2", last_name="Petrov2", passport_number="2200998877")
        self.book = Book.objects.create(title="Test", author="test_author", amount=2)

    def test_reader_list(self):
        response = self.client.get(reverse('reader-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_book_list(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

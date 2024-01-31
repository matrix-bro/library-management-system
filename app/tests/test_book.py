from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
from rest_framework import status
from datetime import date
from app.models.book import Book, BorrowedBooks

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(name='testuser',
                                             email='test@gmail.com',
                                             membership_date=date.today(),
                                             password='testpassword')
        
        self.book = Book.objects.create(title='Test Book', isbn='123456789', published_date=date.today(), genre='Fiction')

        # Authenticate the user for all test cases
        self.client.force_authenticate(user=self.user)
        
    def test_create_book(self):
        url = reverse('create_book')
        data = {'title': 'New Book', 'isbn': '987654321', 'published_date': date.today(), 'genre': 'Non-Fiction'}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_cannot_create_book_with_same_isbn(self):
        url = reverse('create_book')
        data = {'title': 'New Book', 'isbn': '987654321', 'published_date': date.today(), 'genre': 'Non-Fiction'}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

        # testing with same isbn number
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)     # Throws HTTP_400_BAD_REQUEST
        self.assertEqual(Book.objects.count(), 2)

    def test_list_books(self):
        url = reverse('list_books')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_book_by_id(self):
        url = reverse('book_details', args={self.book.book_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_update_book_details(self):
        url = reverse('book_update', args={self.book.book_id})

        data = {
                    "title": "Updated Title",
                    "isbn": "1011",
                    "published_date": "2024-01-30",
                    "genre": "Genre updated",
                    "book_details": {
                        "number_of_pages": 100,
                        "publisher": "Publisher updated",
                        "language": "en"
                    }
                }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Book details updated successfully.')

    def test_update_nonexistent_book(self):
        url = reverse('book_update', args={404})
        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # Borrowed Books
    
    def test_borrow_book(self):
        data = {'borrow_date': date.today()}

        url = reverse('borrow_book', kwargs={'user_id': self.user.user_id, 
                                             'book_id': self.book.book_id})

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BorrowedBooks.objects.count(), 1)

    def test_borrow_nonexistent_book(self):
        url = reverse('borrow_book', kwargs={'user_id': self.user.user_id, 
                                             'book_id': 404})
        
        data = {'borrow_date': date.today()}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_return_book(self):
        BorrowedBooks.objects.create(user=self.user, book=self.book, borrow_date=date.today())
        data = {'return_date': date.today()}

        url = reverse('return_book', args={self.book.book_id})
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Book returned successfully.')

    def test_return_nonexistent_book(self):
        url = reverse('return_book', args={404})

        data = {'return_date': date.today()}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_currently_borrowed_books(self):
        BorrowedBooks.objects.create(user=self.user, book=self.book, borrow_date=date.today())

        url = reverse('currently_borrowed_books')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
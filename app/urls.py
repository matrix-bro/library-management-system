from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app.api import user, book

urlpatterns = [
    # User
    path('register/', user.RegisterUser.as_view(), name='register'),
    path('users/', user.GetAllUsers.as_view(), name='users'),
    path('users/<int:pk>/', user.GetUserById.as_view(), name='user_details'),

    # JWT 
    path('token/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Book
    path('books/create/', book.CreateBook.as_view(), name='create_book'),
    path('books/list/', book.ListBooks.as_view(), name='list_books'),
    path('books/details/<int:pk>/', book.GetBookById.as_view(), name='book_details'),
    path('books/update/<int:pk>/', book.UpdateBookDetails.as_view(), name='book_update'),
]

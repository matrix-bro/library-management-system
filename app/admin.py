from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()
from app.models.book import Book, BookDetails, BorrowedBooks

admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookDetails)
admin.site.register(BorrowedBooks)




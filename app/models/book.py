from django.db import models
from django.conf import settings

class Book(models.Model):
    book_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    published_date = models.DateField()
    genre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

class BookDetails(models.Model):
    detail_id = models.BigAutoField(primary_key=True)
    book = models.OneToOneField(Book, related_name="book_details", on_delete=models.CASCADE)
    number_of_pages = models.PositiveIntegerField()
    publisher = models.CharField(max_length=100)
    language = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "bookdetails"

    def __str__(self):
        return f"Details: {self.book.title}"


class BorrowedBooks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "borrowedbooks"

    def __str__(self):
        return f"{self.user.email} - {self.book.title}"
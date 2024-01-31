from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework import serializers, permissions, status
from app.models.book import Book, BookDetails, BorrowedBooks
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()
from app.services.book_services import update_book_details

  
class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    """
    class Meta:
        model = Book
        fields = ('title', 'isbn', 'published_date', 'genre')

class BookDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model with BookDetails.
    """
    class BookDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = BookDetails
            fields = ('number_of_pages', 'publisher', 'language')  
    
    book_details = BookDetailSerializer()

    class Meta:
        model = Book
        fields = ('title', 'isbn', 'published_date', 'genre', 'book_details')  


class CreateBook(CreateAPIView):
    """
    Endpoint for creating a new book.

    Permissions: Requires authentication
    """
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ListBooks(ListAPIView):
    """
    Endpoint for listing all books.

    Permissions: Requires authentication
    """
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class GetBookById(RetrieveAPIView):
    """
    Endpoint for retrieving details of a specific book by Book ID.

    Permissions: Requires authentication
    """
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Book.objects.all()
    serializer_class = BookDetailsSerializer

class UpdateBookDetails(APIView):
    """
    Endpoint for assiging or updating details of a specific book by Book ID.
    
    Permissions: Requires authentication
    """
    permission_classes = (permissions.IsAuthenticated, )

    def put(self, request, pk):
        book = Book.objects.filter(book_id=pk).first()

        if not book:
            return Response(
                {
                    "message": "Book not found.",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        book_serializer = BookDetailsSerializer(book, data=request.data)

        book_serializer.is_valid(raise_exception=True)

        # service for updating book details
        updated_book = update_book_details(book, **book_serializer.validated_data)

        serializers = BookDetailsSerializer(updated_book)
        
        return Response(
            {
                "message": "Book details updated successfully.",
                "data": serializers.data,
                "code": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
    

# Borrowed Books
    
class BorrowBook(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BorrowedBooks
            fields = ('borrow_date', )

    permission_classes = (permissions.IsAuthenticated, )

    """
    Endpoint for creating a new borrowed book entry.

    Permissions: Requires authentication
    """
    def post(self, request, user_id, book_id):
        # Check if the user and book exists or not
        try:
            user = User.objects.get(user_id=user_id)
            book = Book.objects.get(book_id=book_id)
        except (User.DoesNotExist, Book.DoesNotExist):
            return Response({
                "message": "User or Book not found",
                "code": status.HTTP_404_NOT_FOUND,
            }, status.HTTP_404_NOT_FOUND)
        
        borrowed_book_serializer = self.InputSerializer(data=request.data)
        borrowed_book_serializer.is_valid(raise_exception=True)

        borrow_date = borrowed_book_serializer.validated_data['borrow_date']
        
        # if the book is currently borrowed then return (the book is borrowed by others)
        currently_borrowed = BorrowedBooks.currently_borrowed.filter(book=book)

        if currently_borrowed:
            return Response({
                "message": "Book is being currently borrowed by others.",
                "code": status.HTTP_400_BAD_REQUEST,
            }, status.HTTP_400_BAD_REQUEST)
        

        borrowed_book = BorrowedBooks.objects.create(user=user, book=book, borrow_date=borrow_date)

        return Response(
            {
                "message": "Book borrowed successfully.",
                "code": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
    
class ReturnBook(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BorrowedBooks
            fields = ('return_date', )

        return_date = serializers.DateField(required=True)

    permission_classes = (permissions.IsAuthenticated, )

    """
    Endpoint for updating the return date of a borrowed book.
    
    Permissions: Requires authentication
    """
    def put(self, request, book_id):
        try:
            book = Book.objects.get(book_id=book_id)
            borrowed_book = BorrowedBooks.currently_borrowed.get(book=book)
        except (Book.DoesNotExist, BorrowedBooks.DoesNotExist):
            return Response({
                "message": "Book not found or already returned.",
                "code": status.HTTP_404_NOT_FOUND,
            }, status.HTTP_404_NOT_FOUND)   
        
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return_date = serializer.validated_data['return_date']

        borrowed_book.return_date = return_date
        borrowed_book.save()

        return Response(
            {
                "message": "Book returned successfully.",
                "code": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
    
class CurrentlyBorrowedBooks(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BorrowedBooks
            fields = '__all__'

    permission_classes = (permissions.IsAuthenticated, )

    """
    Endpoint for listing currently borrowed books.

    Permissions: Requires authentication
    """
    def get(self, request):
        currently_borrowed = BorrowedBooks.currently_borrowed.all()

        serializer = self.OutputSerializer(currently_borrowed, many=True)

        return Response(
            {
                "message": "List of currently borrowed books",
                "data": serializer.data,
                "code": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework import serializers, permissions, status
from app.models.book import Book, BookDetails
from rest_framework.response import Response

from app.services.book_services import update_book_details

  
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'isbn', 'published_date', 'genre')

class BookDetailsSerializer(serializers.ModelSerializer):
    class BookDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = BookDetails
            fields = ('number_of_pages', 'publisher', 'language')  
    
    book_details = BookDetailSerializer()

    class Meta:
        model = Book
        fields = ('title', 'isbn', 'published_date', 'genre', 'book_details')  


class CreateBook(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ListBooks(ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class GetBookById(RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Book.objects.all()
    serializer_class = BookDetailsSerializer

class UpdateBookDetails(APIView):
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
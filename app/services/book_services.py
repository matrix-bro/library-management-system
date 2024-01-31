from app.models.book import Book, BookDetails

def update_book_details(book, **kwargs):
    # Update Book
    book.title = kwargs['title']
    book.isbn = kwargs['isbn']
    book.published_date = kwargs['published_date']
    book.genre = kwargs['genre']
    book.save()

    # If there is no Book details, then create it
    # If there is then update it
    book_details = BookDetails.objects.filter(book=book).first()
    if not book_details:
        BookDetails.objects.create(book=book, number_of_pages=kwargs['book_details']['number_of_pages'],
                                    publisher = kwargs['book_details']['publisher'],
                                    language = kwargs['book_details']['language'])
    else:
        book_details.number_of_pages = kwargs['book_details']['number_of_pages']
        book_details.publisher = kwargs['book_details']['publisher']
        book_details.language = kwargs['book_details']['language']
        book_details.save()
    
    return book
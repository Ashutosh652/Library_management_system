from django.contrib import admin
from book.models import Book, BookDetails, BorrowedBooks

admin.site.register(Book)
admin.site.register(BookDetails)
admin.site.register(BorrowedBooks)

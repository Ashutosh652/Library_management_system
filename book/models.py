from django.db import models
from account.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    genre = models.CharField(max_length=255)


class BookDetails(models.Model):
    number_of_pages = models.IntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name="details")


class BorrowedBooks(models.Model):
    borrow_date = models.DateField()
    return_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
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
    borrow_date = models.DateField(null=False, default=datetime.today())
    return_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "book"]

    def clean(self):
        # Validate that a user cannot borrow the same book more than once
        existing_borrowed_book = BorrowedBooks.objects.filter(
            user=self.user, book=self.book
        ).exclude(pk=self.pk)
        if existing_borrowed_book.exists():
            raise ValidationError("This user has already borrowed the same book.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

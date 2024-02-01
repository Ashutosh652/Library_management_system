from rest_framework import serializers
from book.models import Book, BookDetails


class BookListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name="book:books-detail", lookup_field="id"
    )

    class Meta:
        model = Book
        fields = ("id", "detail", "title", "isbn", "published_date", "genre")


class BookDetailSerializer(serializers.ModelSerializer):
    number_of_pages = serializers.IntegerField(
        source="details.number_of_pages", required=False
    )
    publisher = serializers.CharField(source="details.publisher", required=False)
    language = serializers.CharField(source="details.language", required=False)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "isbn",
            "published_date",
            "genre",
            "number_of_pages",
            "publisher",
            "language",
        )

    def create(self, validated_data):
        details_data = validated_data.pop("details", {})
        book_instance = Book.objects.create(**validated_data)
        BookDetails.objects.create(book=book_instance, **details_data)
        return book_instance

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", {})
        instance.title = validated_data.get("title", instance.title)
        instance.isbn = validated_data.get("isbn", instance.isbn)
        instance.published_date = validated_data.get(
            "published_date", instance.published_date
        )
        instance.genre = validated_data.get("genre", instance.genre)
        instance.save()

        # Update or create BookDetails
        details_instance = BookDetails.objects.get(book=instance)
        details_instance.number_of_pages = details_data.get(
            "number_of_pages", details_instance.number_of_pages
        )
        details_instance.publisher = details_data.get(
            "publisher", details_instance.publisher
        )
        details_instance.language = details_data.get(
            "language", details_instance.language
        )
        details_instance.save()

        return instance

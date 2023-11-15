from django.utils import timezone
from rest_framework import serializers
from .models import Book, BookstoreUser, BookCover


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCover
        fields = ['book_id', 'image']
#
# class ImageUploadSerializer(serializers.Serializer):


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publish_date', 'ISBN', 'price']


class BookCreateSchema(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publish_date', 'ISBN', 'price']

    def save(self, validated_data):
        Book(**validated_data).save()


class BookUpdateSchema(serializers.Serializer):
    title = serializers.CharField(required=False)
    author = serializers.CharField(max_length=128, required=False)
    publish_date = serializers.DateField(required=False)
    ISBN = serializers.CharField(max_length=50, required=False)
    price = serializers.DecimalField(decimal_places=2, max_digits=8, required=False)

    def update(self, instance, validated_data):
        instance.update(**validated_data, updated_at=timezone.now())


class UserRegisterSchema(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)





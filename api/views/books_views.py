from datetime import datetime, timedelta

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import Book
from api.serializers import BookSerializer, BookCreateSchema, BookUpdateSchema, ImageSerializer


@swagger_auto_schema(methods=['get'], manual_parameters=[
    openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    openapi.Parameter('author', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    openapi.Parameter('publish_from_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='YYYY-mm-dd'),
    openapi.Parameter('publish_to_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='YYYY-mm-dd'),
    openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER)
])
@api_view(['GET'])
def getBooks(request):
    """
    Get all books
    Query params
    :param: title: string
    :param: author: string
    :param: publish_from_date: string format yyyy-mm-dd
    :param: publish_to_date: string format yyyy-mm-dd
    """
    title = request.GET.get('title')
    author = request.GET.get('author')
    publish_from_date = request.GET.get('publish_from_date')
    publish_to_date = request.GET.get('publish_to_date')

    conditions = {}
    if title:
        conditions['title__icontains'] = title
    if author:
        conditions['author__icontains'] = author
    if publish_from_date:
        if publish_to_date:
            conditions['publish_date__gte'] = datetime.strptime(publish_from_date, '%Y-%m-%d')  # exp 2023-01-01
            conditions['publish_date__lt'] = datetime.strptime(publish_to_date, '%Y-%m-%d') + timedelta(days=1)
        else:
            conditions['publish_date__gte'] = datetime.strptime(publish_from_date, '%Y-%m-%d')
    elif publish_to_date:
        conditions['publish_date__lt'] = datetime.strptime(publish_to_date, '%Y-%m-%d') + timedelta(days=1)

    paginator = PageNumberPagination()
    paginator.page_size = 10
    books = Book.objects.filter(**conditions).all()
    data = paginator.paginate_queryset(books, request)
    serializer = BookSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getBookById(request, book_id: int):
    """
    Get a book by id
    :param book_id: int
    """
    book = Book.objects.filter(pk=book_id).first()
    if not book:
        return Response(status=404, data={'message': 'The book not found'})
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@swagger_auto_schema(method='POST', request_body=BookCreateSchema)
@api_view(['POST'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def createBook(request):
    """
    Create a new book
    """
    payload = request.data
    serializer = BookCreateSchema(data=payload)
    if not serializer.is_valid():
        return Response(status=400, data={'message': 'Payload invalid.'})

    serializer.save(payload)
    return Response(status=200, data={'message': 'Successfully created.',
                                      'book': serializer.data})


@swagger_auto_schema(method='PUT', request_body=BookUpdateSchema)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateBook(request, book_id: int):
    """
    Update the book data with provided id
    :param: book_id: int
    """
    if not request.data:
        return Response(status=400, data={'message': 'Should modify at least 1 field.'})

    book = Book.objects.filter(id=book_id)
    if not book:
        return Response(status=404, data={'message': 'The book not found'})

    payload = BookUpdateSchema(data=request.data)
    if not payload.is_valid():
        return Response(status=400, data={'message': 'Payload invalid.'})

    payload.update(book, request.data)
    return Response(status=200, data={'message': 'Successfully updated.'})


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def deleteBook(request, book_id: int):
    """
    Delete a book with id
    :param book_id: int
    """
    book = Book.objects.filter(id=book_id)
    if not book:
        return Response(status=404, data={'message': 'Book not found.'})

    book.delete()
    return Response(status=200, data={'message': 'Successfully deleted the book'})


@swagger_auto_schema(method='POST', request_body=ImageSerializer)
@api_view(['POST'])
@parser_classes([MultiPartParser])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def upload_image(request):
    """
    Upload the image as a book cover
    """
    serializer = ImageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=400, data={'message': 'Upload failed, form is invalid.'})
    serializer.save()
    return Response(status=200, data={'message': 'Successfully uploaded.'})

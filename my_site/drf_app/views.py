from rest_framework import permissions, viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_app.models import Book, Publisher, Store, Author
from drf_app.serializers import (
    BookSerializer,
    PublisherSerializer,
    StoreSerializer,
    AuthorSerializer
)

"""
Lesson Django REST framework: part 1
"""


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('publisher').prefetch_related('authors').order_by('-price')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.AllowAny]


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.AllowAny]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


"""
Lesson Django REST framework: part 2
"""


@api_view(['GET', 'POST'])
def publishers_list(request):
    match request.method:
        case 'GET':
            pubs = Publisher.objects.all()
            serializer = PublisherSerializer(pubs, many=True)
            return Response(serializer.data)
        case 'POST':
            items = []
            for item in request.data:
                serializer = PublisherSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                    items.append(item)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(items, status=status.HTTP_201_CREATED)


"""
Lesson Django REST framework: part 2 HOMEWORK
"""


@api_view(['GET', 'POST'])
def publisher_by_id(request, publisher_id: int) -> Response:
    publisher = Publisher.objects.filter(id=publisher_id).first()
    match request.method:
        case 'GET':
            if not publisher:
                return Response(
                    f"Publisher with id {publisher_id} not found!",
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = PublisherSerializer(publisher)
            return Response(serializer.data)

        case 'POST':
            if publisher:
                return Response(
                    f"Publisher with ID {publisher_id} already exists!",
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = PublisherSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    f"Publisher created: id = {publisher_id}, data = {request.data}",
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['GET', 'POST'])
def book_by_id(request, book_id: int) -> Response:
    book = Book.objects.filter(id=book_id).first()
    match request.method:
        case 'GET':
            if not book:
                return Response(
                    f"Publisher with id {book_id} not found!",
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = BookSerializer(book)
            return Response(serializer.data)

        case 'POST':
            if book:
                return Response(
                    f"Book with ID {book_id} already exists!",
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    f"Publisher created: id = {book_id}, data = {request.data}",
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

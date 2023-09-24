import logging
import sys

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

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s "
    "[%(name)s:%(funcName)s:%(lineno)s] -> %(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
    stream=sys.stdout,
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

"""
Lesson Django REST framework: part 1
"""


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('publisher').prefetch_related('authors').order_by('-price')
    serializer_class = BookSerializer
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

"""
Create Publisher by id: example
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

"""
Homework: implement "book_by_id handler"
"""

@api_view(['GET', 'POST'])
def book_by_id(request, book_id: int) -> Response:
    book = Book.objects.filter(id=book_id).first()

    match request.method:
        case 'GET':
            if not book:
                return Response(
                    f"Book with id {book_id} not found!",
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

            data = request.data
            data['id'] = book_id

            serializer = BookSerializer(data=data)
            if serializer.is_valid():
                logger.debug(f"Validated data: {serializer.validated_data}")
                new_book = serializer.save()
                return Response(
                    f"Book created: id = {book_id}, data = {new_book}",
                    status=status.HTTP_201_CREATED
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

"""
Lesson DRF part 3: ViewSets
"""

class PublisherViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    queryset = Publisher.objects.all().order_by("-pk")
    serializer_class = PublisherSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request) -> Response:
        """
        - called upon the external GET request to:
        "http://{server_host}:{server_port}/drf_app/publishers/"

        External request example:
            resp = requests.get(url="http://127.0.0.1:8000/publishers/")
        """
        logger.debug("Hello from list method")
        return Response([pub.name for pub in self.queryset])

    def create(self, request) -> Response:
        """
        - called upon the external POST request to:
        "http://{server_host}:{server_port}/drf_app/publishers/"
        - new Publisher instance is created in the Database
        from the *request.data*

        External request example:
            resp = requests.post(
                url="http://127.0.0.1:8000/publishers/",
                json={"name": "PublisherNew"}
            )
        """
        logger.debug("Hello from create method")
        data = request.data
        s = self.serializer_class(data=data)
        if s.is_valid():
            s.save()
            return Response("Saved OK")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk) -> Response:
        """
        - called upon the external GET request to:
        "http://{server_host}:{server_port}/drf_app/publishers/{pk}"
        where *pk* is the *Publisher.pk* in Database
        - returns 200 OK and Publisher's data if the Publisher with specified pk exists
        - returns 404 NOT FOUND if the Publisher with specified pk doesn't exist

        NOTE: *pk* is the default lookup field

        External request example:
            resp = requests.get(url="http://127.0.0.1:8000/publishers/10")
        """
        logger.debug("Hello from retrieve method")
        instance = self.get_object()
        return Response(
            self.serializer_class(instance).data,
            status=status.HTTP_200_OK
        )

    def update(self, request, pk=None) -> Response:
        """
        - called upon the external PUT request to:
        "http://{server_host}:{server_port}/drf_app/publishers/{pk}"
        where *pk* is the *Publisher.pk* in Database.
        - if Publisher with the specified pk has been found - it will be
        Updated with the *request.data* and 200 OK is returned
        - returns 404 NOT FOUND if the Publisher with specified pk doesn't exist
        """
        logger.debug("Hello from update method")
        logger.debug(f"Data: {request.data}")
        super().update(request, pk)  # call of update method from the parent class
        return Response(f"Publisher with pk={pk} has been updated!")

    def partial_update(self, request, pk=None) -> Response:
        """
        It cannot work for Publisher model
        """
        return Response("Hello from partial_update")

    def destroy(self, request, pk=None) -> Response:
        """
        - called upon the external DELETE request to:
        "http://{server_host}:{server_port}/drf_app/publishers/{pk}"
        where *pk* is the *Publisher.pk* in Database.
        - if Publisher with the specified pk has been found - it will be
        Deleted and 200 OK is returned
        - returns 404 NOT FOUND if the Publisher with specified pk doesn't exist
        """
        logger.debug("Hello from destroy method")
        super().destroy(request, pk)
        return Response(f"Publisher with pk={pk} has been deleted!")


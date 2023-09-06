import logging
import sys

from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from my_app.models import Book, Store, Author, Publisher
from my_app.utils import query_debugger
from django.db.models import Prefetch, Subquery
from django.shortcuts import render

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s "
           "[%(name)s:%(funcName)s:%(lineno)s] -> %(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
    stream=sys.stdout,
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)
django_logger = logging.getLogger('django.db.backends')
django_logger.setLevel(logging.DEBUG)
django_logger.addHandler(logging.StreamHandler())

# ---------- Lesson DJANGO ORM 3: SELECT RELATED / PREFETCH RELATED ----------- #


@query_debugger(logger)
def _get_all_books():
    """
    Lesson Django ORM 3: Using select_related for ForeignKey
    """
    queryset = Book.objects.all()
    logger.warning(f"SQL: {str(queryset.query)}")
    """
    Один запрос для заполнения всех книг и, выполняя итерацию каждый раз, 
    мы получаем доступ к издателю, который выполняет другой отдельный запрос.
    Давайте изменим запрос с помощью select_related следующим образом и посмотрим, что произойдет.
    """

    # queryset = Book.objects.select_related("publisher")
    # logger.warning(f"SQL: {str(queryset.query)}")

    return [
        {
            'id': book.id, 'name': book.name,
            # here the additional SQL query is executed to get a publisher name
            'publisher': book.publisher.name,
        }
        for book in queryset
    ]


@query_debugger(logger)
def _get_all_stores():
    """
    Lesson Django ORM 3: Using prefetch_related for ManyToManyField
    """
    # queryset = Store.objects.all()
    # logger.warning(f"SQL 1: {str(queryset.query)}")
    """
    У нас в базе 10 магазинов и в каждом магазине по 10 книг. 
    Здесь происходит один запрос для выборки всех хранилищ, 
    и во время итерации по каждому хранилищу выполняется другой запрос, 
    когда мы получаем доступ к полю books ManyToMany.
    Давайте уменьшим количество запросов с помощью prefetch_related
    """
    queryset = Store.objects.prefetch_related("books")
    logger.warning(f"SQL: {str(queryset.query)}")

    stores = []
    for store in queryset:
        all_books = store.books.all()
        books = [book.name for book in all_books]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return stores


@query_debugger(logger)
def _get_stores_with_expensive_books():
    """
    Lesson Django ORM 3: Using prefetch_related for ManyToManyField
     with Prefetch object
    """
    # queryset = Store.objects.prefetch_related('books')
    # logger.warning(f"SQL: {str(queryset.query)}")
    # stores = []
    # for store in queryset:
    #     # Here we use filter by the Books with specified price range
    #     # and this overrides the first 'prefetch_related' result,
    #     # therefore the 12 queries will be executed!
    #     stores_filtered = store.books.filter(price__range=(250, 300))
    #     books = [book.name for book in stores_filtered]
    #     stores.append({'id': store.id, 'name': store.name, 'books': books})

    # To solve the problem above we need to use special Prefetch
    # object within the 'prefetch_related' call and specify
    # the filter by the ManyToMany relation in 'queryset' param:
    queryset = Store.objects.prefetch_related(
        Prefetch(
            'books',
            queryset=Book.objects.filter(price__range=(250, 300))
        )
    )
    stores = []
    for store in queryset:
        stores_filtered = store.books.all()
        books = [book.name for book in stores_filtered]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return stores


@query_debugger(logger)
def _get_all_publishers():
    """
    Lesson Django ORM 3: Using prefetch_related for Reversed ManyToOne Relation
    """
    # Publisher model doesn't have static 'books' field,
    # but Book model has static 'publisher' field as ForeignKey
    # to the Publisher model. In context of the Publisher
    # model the 'books' is dynamic attribute which provides
    # Reversed ManyToOne relation to the Books
    publishers = Publisher.objects.prefetch_related('books')

    publishers_with_books = []
    for p in publishers:
        books = [book.name for book in p.books.all()]
        publishers_with_books.append(
            {'id': p.id, 'name': p.name, 'books': books}
        )

    return publishers_with_books


# ENDPOINTS
def hello(request: HttpRequest) -> HttpResponse:
    return HttpResponse(f"Hello World!")


def get_all_books(request: HttpRequest) -> HttpResponse:
    books_list = _get_all_books()
    return HttpResponse(f"All Books from Stores:\n {books_list}")


def get_all_stores(request: HttpRequest) -> HttpResponse:
    stores_list = _get_all_stores()
    return HttpResponse(f"All Stores:\n {stores_list}")


def get_stores_with_expensive_books(request: HttpRequest) -> HttpResponse:
    stores_list = _get_stores_with_expensive_books()
    return HttpResponse(f"Stores with expensive books:\n {stores_list}")


def get_all_publishers(request: HttpRequest) -> HttpResponse:
    pubs = _get_all_publishers()
    return HttpResponse(f"All Publishers:\n {pubs}")


# ---------- Lesson DJANGO ORM 4: SUB-QUERIES ----------- #

@query_debugger(django_logger)
def _get_publishers_with_expensive_books():
    """
    Lesson 4: SubQuery example
    """
    expensive_books = Book.objects.filter(price__gte=200)

    # N queries:
    # publishers_ids = [book.publisher.id for book in expensive_books]
    # publishers_with_expensive_books = Publisher.objects.filter(id__in=publishers_ids)

    # Only one query:
    publishers_with_expensive_books = Publisher.objects.filter(
        id__in=Subquery(expensive_books.values('publisher'))
    )
    logger.info(f"SQL: {publishers_with_expensive_books.query}")

    return [item for item in publishers_with_expensive_books.values()]


def get_publishers_with_expensive_books(request: HttpRequest) -> HttpResponse:
    authors = _get_publishers_with_expensive_books()
    return HttpResponse(f"Publishers with expensive books:\n {authors}")


# ---------- Lesson DJANGO VIEWS ----------- #

def get_book_by_id(request: HttpRequest, book_id: int) -> HttpResponse:
    if not (book := Book.objects.filter(id=book_id).first()):
        return HttpResponseNotFound(
            f'<h2>Book by id {book_id} not found</h2>'
        )

    authors = book.authors.all()
    authors = "<h2><p>".join([str(a) for a in authors])
    logger.debug(authors)
    return HttpResponse(
        f"<h1>Found book: {book}, authors: <h2><p>{authors}</h1>"
    )


def _get_authors_with_expensive_books():

    queryset = Author.objects.prefetch_related(
        Prefetch(
            'books',
            queryset=Book.objects.filter(price__range=(250, 300))
        )
    )

    authors = []
    for author in queryset:
        authors_filtered = author.books.all()
        books = [book.name for book in authors_filtered]
        authors.append({'id': author.id, 'first_name': author.first_name, 'last_name': author.last_name,
                        'books': books})

    return authors

# ---------- Lesson DJANGO VIEWS: HOMEWORK ----------- #
def get_expensive_books(request: HttpRequest) -> HttpResponse:
    expensive_books = Book.objects.filter(price__gte=250)
    expensive_books = "<h3><p>".join([str(a) for a in expensive_books])
    return HttpResponse(f"<h3>Expensive books:\n {expensive_books}")


def get_all_authors(request: HttpRequest) -> HttpResponse:
    authors = Author.objects.all()
    authors = "<h3><p>".join([str(a) for a in authors])
    return HttpResponse(f"Authors:\n {authors}")


def get_authors_with_expensive_books(request: HttpRequest) -> HttpResponse:
    authors_list = _get_authors_with_expensive_books()
    authors_list = "<h3><p>".join([str(a) for a in authors_list])
    return HttpResponse(f"Authors with expensive books:\n {authors_list}")
    pass


def get_publisher_by_id(request: HttpRequest, publisher_id: int) -> HttpResponse:
    if not (publisher := Publisher.objects.filter(id=publisher_id).first()):
        return HttpResponseNotFound(
            f'<h2>Publisher by id {publisher_id} not found</h2>'
        )

    books = Book.objects.filter(publisher_id=publisher_id).all()
    books = "<h2><p>".join([str(a) for a in books])
    logger.debug(publisher)
    return HttpResponse(
        f"<h1>Found publisher: {publisher}</h1>  <h1><p>Books Publisher {publisher_id}: <h2><p>{books}"
    )


def get_store_by_id(request: HttpRequest, store_id: int) -> HttpResponse:
    if not (store := Store.objects.filter(id=store_id).first()):
        return HttpResponseNotFound(
            f'<h2>Store by id {store_id} not found</h2>'
        )

    books = store.books.all()
    books = "<h2><p>".join([str(a) for a in books])
    logger.debug(books)
    return HttpResponse(
        f"<h1>Found Store: {store}</h1> <h1><p>Store {store_id} books: <h2><p>S{books}</h2>"
    )


def get_author_by_id(request: HttpRequest, author_id: int) -> HttpResponse:
    if not (author := Author.objects.filter(id=author_id).first()):
        return HttpResponseNotFound(
            f'<h2>Store by id {author_id} not found</h2>'
        )
    return HttpResponse(
        f"<h1>Found author by id {author_id}: {author}</h1>"
    )


# ---------- Lesson DJANGO TEMPLATES ----------- #

def hello_v2(request: HttpRequest) -> HttpResponse:
    """
    Lesson "Django Templates"
    """
    return render(request, "index.html")


def get_first_three_books(request: HttpRequest) -> HttpResponse:
    """
    Lesson "Django Templates"
    """
    keys = ('book1', 'book2', 'book3')
    not_found = 'Not Found'

    match _get_all_books()[:3]:
        case book1, book2, book3:
            context = dict(zip(keys, (book1, book2, book3)))
        case book1, book2:
            context = dict(zip(keys, (book1, book2, not_found)))
        case book1, *_:
            context = dict(zip(keys, (book1, not_found, not_found)))
        case _:
            context = dict.fromkeys(keys, not_found)

    return render(
        request,
        "books1.html",
        context=context
    )


def get_all_books_v2(request: HttpRequest) -> HttpResponse:
    """
    Lesson "Django Templates"
    """
    books_list = _get_all_books()

    return render(
        request,
        "books2.html",
        context={
            'books': books_list
        }
    )


# ---------- Lesson DJANGO TEMPLATES: HOMEWORK ----------- #

@query_debugger(logger)
def _get_only_books_with_authors():
    queryset = Book.objects.prefetch_related(
        Prefetch(
            'authors',
            queryset=Author.objects.filter()
        )
    )
    books = []
    for book in queryset:
        books_filtered = book.authors.all()
        author = [author.first_name for author in books_filtered]
        books.append({'id': book.id, 'name': book.name, 'author': author})

    return books


def get_only_books_with_authors(request: HttpRequest) -> HttpResponse:
    books_with_author = _get_only_books_with_authors()
    return render(request, "books3.html", context={"books_with_author": books_with_author})


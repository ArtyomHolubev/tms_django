from django.urls import path

from . import views

urlpatterns = [
    path('hello', views.hello),
    path('books', views.get_all_books),
    path('stores', views.get_all_stores),
    path('stores_expensive_books', views.get_stores_with_expensive_books),
    path('publisher_expensive_books', views.get_publishers_with_expensive_books),
    path('hello', views.hello),
    path('all_publisher', views.get_all_publishers),
    path('books/<book_id>', views.get_book_by_id),
    path('expensive_books', views.get_expensive_books),
    path('all_authors', views.get_all_authors),
    path('authors_expensive_books', views.get_authors_with_expensive_books),
    path('publisher/<publisher_id>', views.get_publisher_by_id),
    path('store/<store_id>', views.get_store_by_id),
    path('author/<author_id>', views.get_author_by_id),
    path('three_books', views.get_first_three_books),
    path('all_books', views.get_all_books_v2),
    path('books_with_author', views.get_only_books_with_authors),
]

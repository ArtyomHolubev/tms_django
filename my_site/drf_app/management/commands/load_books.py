import random
from django.core.management.base import BaseCommand
from drf_app.models import Publisher, Store, Book, Author


class Command(BaseCommand):
    """
    Эта команда предназначена для вставки издателя, книги, магазина в базу данных.
    Добавляет 5 издателей, 100 книг, 10 магазинов.
    """

    def handle(self, *args, **options):
        Publisher.objects.all().delete()
        Book.objects.all().delete()
        Store.objects.all().delete()

        # создать 5 издателей
        publishers = [Publisher(name=f"Publisher{index}") for index in range(1, 6)]
        Publisher.objects.bulk_create(publishers)

        # создать по 20 книг для каждого издателя
        counter = 0
        books = []
        for publisher in Publisher.objects.all():
            for i in range(20):
                counter = counter + 1
                books.append(Book(name=f"Book{counter}", price=random.randint(50, 300), publisher=publisher))

        Book.objects.bulk_create(books)

        # создать 10 магазинов и вставить по 10 книг в каждый магазин
        books = list(Book.objects.all())
        for i in range(10):
            temp_books = [books.pop(0) for i in range(10)]
            store = Store.objects.create(name=f"Store{i+1}")
            store.books.set(temp_books)
            store.save()

        a1, a2, a3, a4, a5 = [
                    Author.objects.create(
                        first_name=f"Author_{i}_name",
                        last_name=f"Author_{i}_surname",
                        email=f"author.{i}@gmail.com"
                    )
                    for i in range(1, 6)
                ]

        b1, b2, b3, b4, b5 = Book.objects.all()[:5]
        b1.authors.add(a1, a2)
        b2.authors.add(a3, a4)
        b3.authors.add(a5)
        b4.authors.add(a1, a3, a5)
        b5.authors.add(a2, a4)
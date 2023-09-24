import io
from drf_app.models import Book, Publisher, Author
from drf_app.serializers import BookSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

pub = Publisher.objects.last()
book1 = Book.objects.last()
serializer = BookSerializer(book1)
data = serializer.data

content = JSONRenderer().render(data)


JSONParser.parse(content)

stream = io.BytesIO(content)
# stream = io.StringIO(content)
stream.read()
stream.seek(0)
data_from_stream = JSONParser().parse(stream)

serializer.create({'id': 105, 'name': 'NewAnyBook', 'price': 200000, 'publisher': pub})
serializer.update(book1, {'price': 1})


import requests
pub_new_data = {'username': 'vasya', 'password': 'asdasd123123', 'email': 'vasya@mail.com'}
url = 'http://127.0.0.1:8000/auth/users/'
resp = requests.post(url=url, json=pub_new_data)


pub_new_data = {'username': 'vasya', 'asdasd123123': 'asd123123'}
url = 'http://127.0.0.1:8000/auth/jwt/create/'
resp = requests.post(url=url, json=pub_new_data)


import requests
user_data = {'email': 'liza@mail.com', 'password': 'liza23123'}
url = 'http://127.0.0.1:8000/users_app/auth/users/'
resp = requests.post(url=url, json=user_data)

# {
#             "id": 4,
#             "name": "Book4",
#             "price": 246,
#             "publisher": 1,
#             "authors": [
#                 1,
#                 3,
#                 5
#             ]
#         }


# {
#     "id": 112,
#     "name": "NewAnyBook",
#     "price": 200000,
#     "publisher": {"id": 12, "name": "Publisher12"},
#     "authors": {"id": 20, "first_name": "vasya" , "last_name": "vasya", "email": "vasya"}
# }


# {
#     "id": 112,
#     "name": "NewAnyBook",
#     "price": 200000,
#     "publisher_id": 2
# }

from django.contrib.auth.models import User, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, *args, **kwargs):
        response = super().create_user(username, email, password, *args, **kwargs)
        send_mail(subject='Account active',
                  message='Yor account is active',
                  from_email=DEFAULT_FROM_EMAIL,
                  recipient_list=[email]
                  )
        return response


class CustomUser(User):
    objects = UserManager()

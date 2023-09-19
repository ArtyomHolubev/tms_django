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
pub_new_data = {}
url = 'http://127.0.0.1.8000/drf_app/publishers'
resp = requests.post(url=url, json=[pub_new_data])

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

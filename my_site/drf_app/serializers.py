from drf_app.models import Book, Publisher, Store, Author
from rest_framework import serializers

"""
Lesson Django REST framework: part 1
"""

"""
Serializers types:

- serializers.Serializer: Base Serializer class, using it you should specify all needed fields explicitly as:

    class BookSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField(required=True, max_length=300)
        price = serializers.IntegerField(required=True)
        publisher = serializers.CharField(required=True)

- serializers.ModelSerializer: almost the same as serializers.Serializer but
using serializers.ModelSerializer you can specify inner Meta class with 'model'
attribute related to the specific ORM Model and 'fields' attribute which is list
of ORM Model's fields you want to serialize

    class BookSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book  # ORM Model Class
            fields = ['id', 'name', 'price', 'publisher']

Also you can specify the fields explicitly, for example, relationships fields

    class AuthorSerializer(serializers.ModelSerializer):
        publisher = PublisherSerializer()

        class Meta:
            model = Author  # ORM Model Class
            fields = ['id', 'name', 'price', 'publisher']

 Explanation: By default DRF applies the PrimaryKeyRelatedField to the relationship field
 specified in Meta ('publisher') and in this case, after the serialisation, the 'publisher' 
 in Json dict will be only id of the appropriate Publisher object.  
 To change this behaviour we specify 'publisher' field explicitly with the appropriate Serializer type,
 in this case, after the serialisation, the 'publisher' in Json dict will be dict with the appropriate
 Publisher object's fields

 - serializers.HyperlinkedModelSerializer: 

     class BookSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Book  # ORM Model Class
            fields = ['id', 'name', 'price', 'publisher']

 It's almost the same as serializers.ModelSerializer but
 it requires the additional 'url' attribute. When we use serializers.HyperlinkedModelSerializer
 only under the ViewSet, the 'url' attribute value is resolved dynamically.
 In this case we will see on the web-page that relationships values are the html-links 
 which lead to the separate web-pages related to the appropriate relationships objects

"""


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'email']


class BookSerializer(serializers.ModelSerializer):
    """
    Lesson Django REST framework: part 2
    """

    publisher = PublisherSerializer()
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'price', 'publisher', 'authors']

    def create(self, validated_data):
        """
        Create new Book instance
        """
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Book` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.publisher = validated_data.get('publisher', instance.publisher)
        if authors := validated_data.get('authors'):
            instance.authors.add(authors)
        instance.save()
        return instance


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'books']

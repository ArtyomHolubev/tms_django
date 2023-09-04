from django.db import models

#
# class Students(models.Model):
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)


class User(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=6)
    nationality = models.TextField()


class Post(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")


class Like(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name}, {self.last_name}$, [email: {self.email}]'


class Book(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)

    class Meta:
        default_related_name = 'books'

    def __str__(self):
        return f'{self.name}, {self.price}$, [publisher: {self.publisher}]'


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)

    class Meta:
        default_related_name = 'stores'

    def __str__(self):
        return self.name

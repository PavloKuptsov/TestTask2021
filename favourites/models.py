from django.db import models


class Author(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    def __str__(self):
        return f'User id:{self.id} @{self.username}'


class Tweet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    retweet_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    quote_count = models.IntegerField(default=0)
    language = models.CharField(max_length=5)

    def __str__(self):
        return f'Tweet id:{self.id} by @{self.author.username} created at {self.created_at}'

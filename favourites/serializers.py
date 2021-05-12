from rest_framework import serializers
from favourites.models import Author
from favourites.models import Tweet


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id',
            'name',
            'username',
        )


class TweetShortSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)

    class Meta:
        model = Tweet
        fields = (
            'id',
            'text',
            'created_at',
            'retweet_count',
            'reply_count',
            'author',
        )


class TweetSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)

    class Meta:
        model = Tweet
        fields = '__all__'


class TweetBookmarkingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ('id',)



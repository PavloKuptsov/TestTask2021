from rest_framework import viewsets, status, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from favourites.client import Client
from favourites.models import Tweet
from favourites.serializers import TweetSerializer
from favourites.serializers import TweetShortSerializer
from favourites.serializers import TweetBookmarkingSerializer


class TweetViewSetMixin:
    def get_serializer_class(self):
        if self.action == 'list':
            return TweetShortSerializer
        if self.action == 'create':
            return TweetBookmarkingSerializer
        return TweetSerializer


class FavouritesViewSet(TweetViewSetMixin, viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', 'author__name', 'author__username']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.sort_queryset(queryset, request.query_params)
        page = self.paginate_queryset(queryset)

        if page is None:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        tweet_id = request.data.get('id')
        tweet = Client.get_tweet(tweet_id)
        tweet.author.save()
        tweet.save()
        return Response(status=status.HTTP_201_CREATED)

    def sort_queryset(self, queryset, query_params):
        sortable_fields = ('created_at',
                           'retweet_count',
                           'reply_count',
                           'like_count',
                           'quote_count')
        sort_by = query_params.get('sort_by', 'created_at')
        sort_order = query_params.get('sort_order', 'desc')
        sort_expression = ('-' if sort_order == 'desc' else '') + \
                          (sort_by if sort_by in sortable_fields else 'created_at')
        return queryset.order_by(sort_expression)


class TweetsViewSet(TweetViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Tweet.objects.all()

    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search', '')
        username = request.query_params.get('username', '')
        queryset = self.get_queryset(search, username)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        tweet_id = kwargs.get('pk', 0)
        queryset = Client.get_tweet(tweet_id)
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)

    def get_queryset(self, search='', username=''):
        return Client.search_tweets(search=search, username=username)

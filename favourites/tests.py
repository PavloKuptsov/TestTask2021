from datetime import datetime, timedelta
from unittest.mock import MagicMock

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from favourites.client import Client
from favourites.models import Tweet, Author
from favourites.views import FavouritesViewSet

tweet_to_add = Tweet(
            id=4,
            text='Tweet four text',
            created_at=datetime.utcnow(),
            retweet_count=0,
            reply_count=0,
            like_count=0,
            quote_count=0,
            language='uk',
            author=Author(
                id=4,
                name='quad',
                username='quad'
            )
        )


class FavouritesTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('username', 'Pas$w0rd')
        cls.factory = APIRequestFactory()
        tweet1 = Tweet(
            id=1,
            text='Tweet one text',
            created_at=datetime.utcnow() - timedelta(days=2),
            retweet_count=10,
            reply_count=0,
            like_count=10,
            quote_count=5,
            language='en',
            author=Author(
                id=1,
                name='Author Name',
                username='authorname'
            )
        )
        tweet1.author.save()
        tweet1.save()

        tweet2 = Tweet(
            id=2,
            text='Tweet two text',
            created_at=datetime.utcnow() - timedelta(days=1),
            retweet_count=5,
            reply_count=5,
            like_count=0,
            quote_count=0,
            language='uk',
            author=Author(
                id=2,
                name='Silly Author Name',
                username='sillyauthorname'
            )
        )
        tweet2.author.save()
        tweet2.save()

        tweet3 = Tweet(
            id=3,
            text='Tweet three text',
            created_at=datetime.utcnow(),
            retweet_count=0,
            reply_count=10,
            like_count=5,
            quote_count=10,
            language='fr',
            author=Author(
                id=3,
                name='Jerry the World Crusher',
                username='saygoodbyetoyourworld'
            )
        )
        tweet3.author.save()
        tweet3.save()

    def test_not_authenticated(self):
        request = self.factory.get('')
        view = FavouritesViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 401)

    def test_favourites_list(self):
        request = self.factory.get('')
        force_authenticate(request, user=self.user)
        view = FavouritesViewSet.as_view({'get': 'list'})
        response = view(request)
        results = response.data['results']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(results), 3)
        self.assertEqual([item['id'] for item in results], [3, 2, 1])

    def test_favourite(self):
        request = self.factory.get('')
        force_authenticate(request, user=self.user)
        view = FavouritesViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=3)
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], 3)
        self.assertEqual(data['text'], 'Tweet three text')
        self.assertEqual(data['author']['username'], 'saygoodbyetoyourworld')
        self.assertEqual(data['language'], 'fr')

    def test_favourites_list_search(self):
        request = self.factory.get('', data={'search': 'two'})
        force_authenticate(request, user=self.user)
        view = FavouritesViewSet.as_view({'get': 'list'})
        response = view(request)
        results = response.data['results']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 2)

    def test_favourites_list_retweet_sort(self):
        request = self.factory.get('', data={'sort_by': 'retweet_count'})
        force_authenticate(request, user=self.user)
        view = FavouritesViewSet.as_view({'get': 'list'})
        response = view(request)
        results = response.data['results']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(results), 3)
        self.assertEqual([item['id'] for item in results], [1, 2, 3])

    def test_favourites_list_quote_sort_asc(self):
        request = self.factory.get('', data={'sort_by': 'quote_count', 'sort_order': 'asc'})
        force_authenticate(request, user=self.user)
        view = FavouritesViewSet.as_view({'get': 'list'})
        response = view(request)
        results = response.data['results']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(results), 3)
        self.assertEqual([item['id'] for item in results], [2, 1, 3])

    def test_favourite_delete(self):
        request = self.factory.delete('')
        force_authenticate(request, user=self.user)
        view = FavouritesViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=2)
        self.assertEqual(response.status_code, 204)
        tweets = Tweet.objects.all()
        self.assertEqual(len(tweets), 2)
        self.assertNotIn(2, [tweet.id for tweet in tweets])

    def test_favourite_create(self):
        request = self.factory.post('', data={'id': 20})
        force_authenticate(request, user=self.user)
        view = FavouritesViewSet.as_view({'post': 'create'})
        client = Client
        client.get_tweet = MagicMock(return_value=tweet_to_add)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        tweet = Tweet.objects.get(id=4)
        self.assertEqual(tweet.text, 'Tweet four text')



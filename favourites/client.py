import requests
from rest_framework import status
from rest_framework.exceptions import ValidationError

from favourites.exceptions import NotAuthorized, NotFound
from favourites.models import Tweet, Author
from socialTestTask import settings


class Client:
    token = f'Bearer {settings.PLATFORM_TOKEN}'
    base_url = 'https://api.twitter.com/2'
    expansions = 'expansions=author_id&tweet.fields=created_at,public_metrics,lang'

    @classmethod
    def make_request(cls, details_url):
        headers = {'Authorization': cls.token,
                   'Content-Type': 'application/json'}
        url = cls.base_url + details_url
        response = requests.get(url, headers=headers)
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise NotAuthorized

        payload = response.json()
        if 'errors' in payload:
            if payload['errors'] and payload.get('title') == 'Invalid Request':
                message = payload['errors'].pop().get('message')
                raise ValidationError(message)

            if payload['errors'] and \
                    payload['errors'].pop().get('title') == 'Not Found Error':
                raise NotFound

        return payload

    @classmethod
    def search_tweets(cls, search='', username=''):
        # Little dirty hack to get some feed without the need to look into streams
        if not (search or username):
            search = 'cat'  # of course, it's a cat; twitter is made for cats

        details_url = f'/tweets/search/recent?query={search}'

        if username:
            details_url += f' from:{username}'

        details_url += f'&max_results=10&{cls.expansions}'
        response = cls.make_request(details_url)

        tweets = []
        user_data = response.get('includes', {}).get('users', [])
        users_dict = {user['id']: user for user in user_data}

        for tweet_dict in response.get('data', []):
            author_id = tweet_dict['author_id']
            tweets.append(cls._dict_to_model(tweet_dict, users_dict[author_id]))

        return tweets

    @classmethod
    def get_tweet(cls, tweet_id):
        details_url = f'/tweets/{tweet_id}?{cls.expansions}'
        response = cls.make_request(details_url)
        user_data = response.get('includes', {}).get('users', [])
        users_dict = {user['id']: user for user in user_data}
        print(response)
        author_id = response['data']['author_id']
        return cls._dict_to_model(response['data'], users_dict[author_id])

    @classmethod
    def _dict_to_model(cls, tweet_dict, user_dict):
        tweet = Tweet(
            id=tweet_dict['id'],
            text=tweet_dict['text'],
            created_at=tweet_dict['created_at'],
            retweet_count=tweet_dict['public_metrics']['retweet_count'],
            reply_count=tweet_dict['public_metrics']['reply_count'],
            like_count=tweet_dict['public_metrics']['like_count'],
            quote_count=tweet_dict['public_metrics']['quote_count'],
            language=tweet_dict['lang'],
            author=Author(
                id=user_dict['id'],
                name=user_dict['name'],
                username=user_dict['username']
            )
        )

        return tweet

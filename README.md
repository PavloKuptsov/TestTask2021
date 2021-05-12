# Test task

Due to lack of time and expertise, this task only has backend elements (there's graphical API tool provided by Django REST framework).

# Summary
This BE can retrieve tweets from TwitterAPI v2, mark them as Favourites (essentially saving some basic information about them to a local PostgreSQL DB).

# Endpoints

All endpoints require Basic HTTP Auth.

`GET /tweets/` - endpoint that shows 10 random recent tweets.
Accepts two query string parameters:
`search` - text search query
`username` - a way to further narrow down search by inputting a twitter handle. 
Due to limitation of a hobbyist API access, search is only conducted through the last week of tweets.

`GET /tweets/<tweet_id>/` - shows a little more information about a single tweet by its ID.

`GET /favourites/` - shows a paginated list of favourited tweets.
Accepts query string parameters:
`search` - text search query
`sort_by` - can be one of the following: `created_at, retweet_count, reply_count, like_count, quote_count`. The default value is `created_at`.
`sort_order` - can be `asc` or `desc`. The default value is `desc`.

`POST /favourites/` - marks a tweet as a favourite.
Accepts request body `{"id": <tweet_id>}`

`GET /favourites/<tweet_id>/` - shows a little more information about a single favourited tweet by its ID.

`DELETE /favourites/<tweet_id>/` - removes a tweet from favourites.
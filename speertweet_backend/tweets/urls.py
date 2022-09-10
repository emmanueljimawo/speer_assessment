from django.urls import path

from .views import (
    TweetListCreateAPIView,
    TweetDetailAPIView,
    LikeTweetAPIView,
    UserTweetListAPIView,
    RecentTweetsAPIView
)

urlpatterns = [
    path('', TweetListCreateAPIView.as_view(), name='tweet_list_create'),
    path('<uuid>/', TweetDetailAPIView.as_view(), name='tweet_detail'),
    path('<uuid>/tweet/', LikeTweetAPIView.as_view(), name='like_tweet'),
    path('recent/', RecentTweetsAPIView.as_view(), name='recent_tweets'),
    path('user/<uuid>/', UserTweetListAPIView.as_view(), name='get_user_tweets')
]
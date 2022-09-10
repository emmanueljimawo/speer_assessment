from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as s
from django.shortcuts import get_object_or_404

from .models import Tweet
from .serializers import TweetSerializer
from .permissions import IsAuthorOrReadOnly


class TweetListCreateAPIView(ListCreateAPIView):
    """
    Lists the currently logged in users tweets with a GET and allows a user to 
    create a new tweet with TWEET. Must be logged in to access this route.
    EXAMPLE:
        GET -> /tweets/ -> return a list of tweets
        TWEET -> /tweets/ -> create new tweet
    """
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return all tweets for logged in user.
        """
        return Tweet.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class TweetDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Selects tweet by UUID and displays it's details. Anon users able to read tweet
    details with GET. Must be authenticated and be the owner of the tweet to make 
    PUT and DELETE requests.
    EXAMPLE:
        GET -> /tweets/<uuid>/ -> return tweet details
        PUT -> /tweets/<uuid>/ -> make an edit to the tweet text (if owner)
        DELETE -> /tweets/<uuid>/ -> delete tweet (if owner)
    """
    queryset = Tweet.objects.all()
    lookup_field = 'uuid'

    serializer_class = TweetSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        return serializer.save(edited=True)


class LikeTweetAPIView(APIView):
    """
    Allows any authenticated user to like (like) a tweet. This endpoint increments
    a tweets likes by 1.
    NOTE:   Currently a user can like the same tweet as many times as they like. 
            This could be avoided by pulling the likes out into their own table 
            with one to one FK to a tweet and user, would require a check before
            likening tweet (some indexing on the table would be a good idea too).
    EXAMPLE:
        PUT -> /tweets/<uuid>/like/ -> increment tweet likes by 1
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, uuid):
        """
        Increment tweet likes by 1.
        """
        tweet = get_object_or_404(Tweet, uuid=uuid)
        tweet.likes += 1
        tweet.save()
        return Response(status=s.HTTP_200_OK)


class UserTweetListAPIView(ListAPIView):
    """
    """
    serializer_class = TweetSerializer

    def get_queryset(self):
        return Tweet.objects.order_by('-date_created').filter(author__uuid=self.kwargs['uuid'])


class RecentTweetsAPIView(ListAPIView):
    """
    """
    serializer_class = TweetSerializer
    queryset = Tweet.objects.order_by('-date_created').all()
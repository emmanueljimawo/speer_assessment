from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status as s
from uuid import uuid4
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from .models import Tweet
from .serializers import TweetSerializer

# Create your tests here.



User = get_user_model()


class TweetModelTest(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(
            username='test', password='password')

    def test_tweet_create(self):
        p = Tweet.objects.create(
            text='tweet',
            author=self.author,
            likes=0)
        self.assertEqual(p.text, 'tweet')
        self.assertEqual(p.author.uuid, self.author.uuid)
        self.assertEqual(p.likes, 0)


class TweetListCreateTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='password')
        Tweet.objects.create(text='tweet1', author=user)
        Tweet.objects.create(text='tweet2', author=user)
        Tweet.objects.create(text='tweet3', author=user)
        return super().setUpTestData()

    def setUp(self):
        res = self.client.tweet(reverse('token_login'), data={
            'username': 'test',
            'password': 'password',
        })
        self.token = res.data.get('access')
        self.author = User.objects.get(pk=1)

    def test_tweet_list(self):
        res = self.client.get(reverse('tweet_list_create'),
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')
        tweets = TweetSerializer(
            instance=Tweet.objects.filter(author=self.author), many=True)

        self.assertEqual(res.status_code, s.HTTP_200_OK)
        self.assertListEqual(tweets.data, res.data)

    def test_tweet_list_unauth(self):
        res = self.client.get(reverse('tweet_list_create'))

        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)

    def test_tweet_list_filter(self):
        user2 = User.objects.create_user(username='test2', password='password')
        Tweet.objects.create(text='tweet', author=user2)

        res = self.client.get(reverse('tweet_list_create'),
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')
        tweets = TweetSerializer(
            instance=Tweet.objects.filter(author=self.author), many=True)

        self.assertEqual(res.status_code, s.HTTP_200_OK)
        self.assertListEqual(tweets.data, res.data)

    def test_create_new_tweet(self):
        res = self.client.tweet(
            reverse('tweet_list_create'),
            data={'text': 'My new tweet'},
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        self.assertEqual(res.status_code, s.HTTP_201_CREATED)

        new_tweet = TweetSerializer(
            instance=Tweet.objects.get(text='My new tweet'))
        self.assertDictEqual(new_tweet.data, res.data)


class TweetDetailView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='password')
        Tweet.objects.create(text='tweet1', author=user)
        Tweet.objects.create(text='tweet2', author=user)
        Tweet.objects.create(text='tweet3', author=user)
        User.objects.create_user(username='test2', password='password')

    def setUp(self):
        res = self.client.tweet(reverse('token_login'), data={
            'username': 'test',
            'password': 'password',
        })
        self.token = res.data.get('access')
        self.author = User.objects.get(pk=1)

        res = self.client.tweet(reverse('token_login'), data={
            'username': 'test2',
            'password': 'password',
        })
        self.token2 = res.data.get('access')

    def test_detail_view_unauth(self):
        p = Tweet.objects.get(pk=1)
        ps = TweetSerializer(instance=p)

        res = self.client.get(reverse('tweet_detail', kwargs={'uuid': p.uuid}))

        self.assertEqual(res.status_code, s.HTTP_200_OK)
        self.assertDictEqual(ps.data, res.data)

    def test_detail_view_auth(self):
        p = Tweet.objects.get(pk=1)
        ps = TweetSerializer(instance=p)

        res = self.client.get(reverse('tweet_detail', kwargs={'uuid': p.uuid}),
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(res.status_code, s.HTTP_200_OK)
        self.assertDictEqual(ps.data, res.data)

    def test_delete_no_user(self):
        p = Tweet.objects.get(pk=1)
        res = self.client.delete(
            reverse('tweet_detail', kwargs={'uuid': p.uuid}))

        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Tweet.objects.get(pk=1).id, p.id)

    def test_delete_wrong_user(self):
        p = Tweet.objects.get(pk=1)
        res = self.client.delete(reverse('tweet_detail', kwargs={'uuid': p.uuid}),
                                 HTTP_AUTHORIZATION=f'Bearer {self.token2}')

        self.assertEqual(res.status_code, s.HTTP_403_FORBIDDEN)
        self.assertEqual(Tweet.objects.get(pk=1).id, p.id)

    def test_delete(self):
        p = Tweet.objects.get(pk=1)
        res = self.client.delete(reverse('tweet_detail', kwargs={'uuid': p.uuid}),
                                 HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(res.status_code, s.HTTP_204_NO_CONTENT)
        with self.assertRaises(Tweet.DoesNotExist):
            Tweet.objects.get(pk=1)

    def test_update(self):
        p = Tweet.objects.get(pk=1)
        self.assertFalse(p.edited)

        res = self.client.put(reverse('tweet_detail', kwargs={'uuid': p.uuid}),
                              data={'text': 'edited text'},
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(res.status_code, s.HTTP_200_OK)

        p = Tweet.objects.get(pk=1)
        self.assertEqual(p.text, 'edited text')
        self.assertTrue(p.edited)

    def test_update_no_user(self):
        p = Tweet.objects.get(pk=1)
        res = self.client.put(reverse('tweet_detail', kwargs={'uuid': p.uuid}),
                              data={'text': 'edited text'})

        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)

    def test_update_wrong_user(self):
        p = Tweet.objects.get(pk=1)
        res = self.client.put(reverse('tweet_detail', kwargs={'uuid': p.uuid}),
                              data={'text': 'edited text'},
                              HTTP_AUTHORIZATION=f'Bearer {self.token2}')

        self.assertEqual(res.status_code, s.HTTP_403_FORBIDDEN)

    def test_bad_update(self):
        p = Tweet.objects.get(pk=1)
        self.assertEqual(p.likes, 0)

        res = self.client.put(reverse('tweet_detail', kwargs={'uuid': p.uuid}),
                              data={'likes': 1000},
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(res.status_code, s.HTTP_400_BAD_REQUEST)

        p = Tweet.objects.get(pk=1)
        self.assertEqual(p.likes, 0)


class LikeTweetViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='password')
        Tweet.objects.create(text='tweet1', author=user)
        Tweet.objects.create(text='tweet2', author=user)
        Tweet.objects.create(text='tweet3', author=user)
        User.objects.create_user(username='test2', password='password')

    def setUp(self):
        res = self.client.tweet(reverse('token_login'), data={
            'username': 'test',
            'password': 'password',
        })
        self.token = res.data.get('access')
        self.author = User.objects.get(pk=1)

        res = self.client.tweet(reverse('token_login'), data={
            'username': 'test2',
            'password': 'password',
        })
        self.token2 = res.data.get('access')

    def test_like(self):
        p = Tweet.objects.get(pk=1)
        self.assertEqual(p.likes, 0)

        res = self.client.put(reverse('like_tweet', kwargs={'uuid': p.uuid}),
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(res.status_code, s.HTTP_200_OK)

        p = Tweet.objects.get(pk=1)
        self.assertEqual(p.likes, 1)

    def test_like_unauth(self):
        p = Tweet.objects.get(pk=1)
        self.assertEqual(p.likes, 0)

        res = self.client.put(reverse('like_tweet', kwargs={'uuid': p.uuid}))
        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)

        p = Tweet.objects.get(pk=1)
        self.assertEqual(p.likes, 0)

    def test_like_404(self):
        res = self.client.put(reverse('like_tweet', kwargs={'uuid': uuid4()}),
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(res.status_code, s.HTTP_404_NOT_FOUND)




class UserTweetListAPIViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='password')
        Tweet.objects.create(text='tweet1', author=user)
        Tweet.objects.create(text='tweet2', author=user)
        Tweet.objects.create(text='tweet3', author=user)
        user = User.objects.create_user(username='test2', password='password')

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

    def test_list_tweets(self):
        tweets = TweetSerializer(instance=Tweet.objects.order_by('-date_created').filter(
            author__uuid=self.user.uuid), many=True)
        res = self.client.get(
            reverse('get_user_tweets', kwargs={'uuid': self.user.uuid}))

        self.assertDictEqual(tweets.data[0], res.data[0])
        self.assertDictEqual(tweets.data[1], res.data[1])
        self.assertDictEqual(tweets.data[2], res.data[2])

    def test_no_tweets(self):
        res = self.client.get(
            reverse('get_user_tweets', kwargs={'uuid': self.user2.uuid}))

        self.assertEqual(res.data, [])

    def test_bad_uuid(self):
        res = self.client.get(
            reverse('get_user_tweets', kwargs={'uuid': uuid4()}))
        self.assertEqual(res.data, [])
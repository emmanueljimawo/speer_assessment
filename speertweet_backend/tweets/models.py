from django.db import models
from uuid import uuid4

# Create your models here.


class Tweet(models.Model):

    uuid = models.UUIDField(default=uuid4, null=False)
    text = models.CharField(max_length=250, null=False)
    likes = models.IntegerField(default=0, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        'users.User', related_name='tweets', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['date_created', '-likes']),
            models.Index(fields=['author_id', 'date_created'])
        ]

    def __str__(self):
        return f'<Post uuid={self.uuid} author={self.author}>'

    def get_comment_count(self):
        """
        Return the number of comments on this post.
        """
        return self.comments.count()

from rest_framework import serializers

from . import models





class TweetSerializer(serializers.ModelSerializer):
    """
    Serializer that provides an overview of the Tweet model. 
    """
    author = serializers.ReadOnlyField(source='author.username')
   

    class Meta:
        model = models.Tweet
        fields = ['uuid', 'text', 'author', 'likes',
                  'date_created']
        read_only_fields = ['uuid', 'author', 'date_created', 'likes']
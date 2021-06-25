from rest_framework import serializers
from posts.models import Post

class PostsSerializer(serializers.ModelSerializer):

    class Meta:

        model = Post
        fields = ('id', 'post_title', 'post_body', 'post_img', 'date', 'post_slug', 'category')

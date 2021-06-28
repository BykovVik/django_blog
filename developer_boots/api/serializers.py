from rest_framework import serializers
from posts.models import Post, Category, AppUser

class PostSerializer(serializers.ModelSerializer):

    class Meta:

        model = Post
        fields = ('id', 'post_title', 'date', 'category')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category
        fields = ('id', 'category_name')

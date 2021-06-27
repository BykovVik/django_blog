from django.http import JsonResponse
from posts.models import Post, Category, AppUser
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_posts(request):
    if request.method == 'GET':
        all_posts = Post.objects.all()
        serializer = PostSerializer(all_posts, many=True)
        return Response(serializer.data)

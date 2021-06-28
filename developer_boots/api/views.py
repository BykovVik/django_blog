from posts.models import Post, Category, AppUser
from .serializers import PostSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView



class ApiCategory(APIView):

    def get(self, request):

        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        permission_classes = (IsAdminUser,)
        return Response(serializer.data)


class ApiPosts(APIView):

    def get(self, request):

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        permission_classes = (IsAdminUser,)
        return Response(serializer.data)
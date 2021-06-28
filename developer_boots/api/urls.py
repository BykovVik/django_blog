from django.urls import path
from .views import ApiCategory, ApiPosts

urlpatterns = [

    path('posts/', ApiPosts.as_view()),
    path('category/', ApiCategory.as_view())

]
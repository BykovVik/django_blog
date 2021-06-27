from django.urls import path
from .views import api_posts

urlpatterns = [

    path('posts/', api_posts)

]
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Category(models.Model):

    id = models.AutoField(unique=True, primary_key=True)
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name


class Post(models.Model):

    id = models.AutoField(unique=True, primary_key=True)
    post_title = models.CharField(unique=True, max_length=256)
    post_slug = models.SlugField(max_length=256, unique=True, null=True, blank=True)
    post_img = models.ImageField(upload_to='uploads/', default=None)
    post_body = RichTextUploadingField()
    date = models.DateTimeField()
    category_title = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = TaggableManager()

    class Meta:

        ordering = ['-date']

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse('one_post',
            args = [
                self.category_title,
                self.post_slug
            ]
        )


class Static_page(models.Model):

    id = models.AutoField(unique=True, primary_key=True)
    url = models.CharField(unique=True, max_length=256)
    title = models.CharField(max_length=256)
    body = RichTextUploadingField()


    def __str__(self):
        return self.title


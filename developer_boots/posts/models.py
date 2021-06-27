from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager



class AppUser(AbstractUser):
    
    is_actived = models.BooleanField(default=True, db_index=True, verbose_name="Прошел активацию?")
    send_message = models.BooleanField(default=True, verbose_name="Слать оповещение о новых комментариях?")

    class Meta(AbstractUser.Meta):

        pass



class Category(models.Model):

    id = models.AutoField(unique=True, primary_key=True)
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name

    class Meta:

        verbose_name_plural = "Категории"
        verbose_name = "Категория"


class Post(models.Model):

    id = models.AutoField(unique=True, primary_key=True)
    post_title = models.CharField(unique=True, max_length=256)
    slug = models.SlugField(max_length=256, unique=True, null=True, blank=True)
    post_img = models.ImageField(upload_to='post_image/', default=None)
    post_body = RichTextUploadingField()
    date = models.DateTimeField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):

        return self.post_title

    def get_absolute_url(self):

        return reverse('one_post',
            args = [
                self.category,
                self.slug
            ]
        )

    def delete(self, *args, **kwargs):

        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:

        verbose_name_plural = "Публикации"
        verbose_name = "Публикация"
        ordering = ['-date']



class Static_page(models.Model):

    id = models.AutoField(unique=True, primary_key=True)
    url = models.CharField(unique=True, max_length=256)
    title = models.CharField(max_length=256)
    body = RichTextUploadingField()


    def __str__(self):
        return self.title

    class Meta:

        verbose_name_plural = "Статические страницы"
        verbose_name = "Статическая страница"



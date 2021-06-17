from django.contrib import admin
from .models import Category, Post, Static_page

class PostAdmin(admin.ModelAdmin):

    prepopulated_fields = {
        'post_slug': ('post_title',)
    }
    
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Static_page)
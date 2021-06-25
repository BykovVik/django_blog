from django.contrib import admin
from .models import Category, Post, Static_page, AppUser

class PostAdmin(admin.ModelAdmin):

    list_display = ('id', 'post_title', 'post_slug', 'date', 'category_id')
    list_display_links = ('id', 'post_title')
    prepopulated_fields = {
        'post_slug': ('post_title',)
    }
    
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Static_page)
admin.site.register(AppUser)
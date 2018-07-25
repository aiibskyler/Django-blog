from django.contrib import admin
from .models import BlogType, Article


# Register your models here.
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'blog_type', 'created_time', 'last_updated_time')
    ordering = ('-id',)  # -号倒序

# admin.site.register(Article, ArticleAdmin)

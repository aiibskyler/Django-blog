from django.contrib import admin
from .models import BlogType, Article, ReadNum


# Register your models here.
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'get_read_num', 'blog_type', 'created_time', 'last_updated_time')
    ordering = ('-id',)  # -号倒序

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'blog')

# admin.site.register(Article, ArticleAdmin)

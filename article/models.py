from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail


# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Article(models.Model,ReadNumExpandMethod):
    title = models.CharField(verbose_name='标题', max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE, verbose_name='博客类型')
    content = RichTextUploadingField()
    read_details = GenericRelation(ReadDetail)
    # read_num = models.IntegerField(default=0)
    created_time = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    last_updated_time = models.DateTimeField(verbose_name='更新日期', auto_now=True)




    def __str__(self):
        return '<Article: %s>' % self.title

    class Meta:
        ordering = ['-created_time']


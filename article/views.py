from django.shortcuts import render, render_to_response, get_object_or_404
from .models import Article, BlogType
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read


# Create your views here.
# def article_detail(request, article_id):
#     try:
#         article = Article.objects.get(id=article_id)
#         context = {
#             'article_obj': article,
#         }  # 这里跟教程不一样，这是新的改动
#         # return render(request, "article_detail.html", context)
#         return render(request, "article_detail.html", context)
#     except Article.DoesNotExist:
#         raise Http404("页面不存在")
#     # return HttpResponse('<h2>文章标题id: %s </h2> <br> <p> 文章内容：%s </p>' % (article.title,article.content))


# 使用simple_article_detail中

def get_blog_list_common_data(request, article_all_list):
    paginator = Paginator(article_all_list, settings.EACH_PAGE_BLOG_NUM)
    page_num = request.GET.get('page', 1)  # 获取url页面参数（GET请求）
    page_of_articles = paginator.get_page(page_num)

    # 获取博客数量
    '''
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Article.objects.filter(blog_type = blog_type).count()
        blog_types_list.append(blog_type)'''
    # 获取日期归档对应的数量

    blog_dates = Article.objects.dates('created_time', 'month', order="DESC") \
        .annotate(blog_count=Count('created_time'))
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Article.objects.filter(created_time__year=blog_date.year,
                                            created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['articles'] = page_of_articles.object_list
    # context['blog_types'] = blog_types_list
    context['page_of_articles'] = page_of_articles
    context['articles_count'] = Article.objects.all().count()
    # context['blog_types'] = BlogType.objects.all()
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('article'))
    # context['blog_dates'] = Article.objects.dates('created_time', 'month', order='DESC')
    context['blog_dates'] = blog_dates_dict
    return context


def article_list(request):
    # articles = Article.objects.filter(is_deleted=False)
    article_all_list = Article.objects.all()
    context = get_blog_list_common_data(request, article_all_list)
    return render(request, "article_list.html", context)


def blog_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    article_all_list = Article.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, article_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog_with_type.html', context)


def articles_with_date(request, year, month):
    article_all_list = Article.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, article_all_list)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog_with_date.html', context)


def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    read_cookie_key = read_statistics_once_read(request, article)
    context = {}
    context['article'] = article
    context['previous_blog'] = Article.objects.filter(created_time__gt=article.created_time).last()
    context['next_blog'] = Article.objects.filter(created_time__lt=article.created_time).first()
    response = render(request, "article_detail.html", context)
    response.set_cookie(read_cookie_key, 'true', max_age=60)

    return response

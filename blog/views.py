import datetime
from django.shortcuts import render_to_response
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from article.models import Article
from django.utils import timezone


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Article.objects\
        .filter(read_details__date__lt=today, read_details__date__gte=date)\
        .values('id', 'title')\
        .annotate(read_num_sum=Sum('read_details__read_num'))\
        .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Article)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)
        print('calculate')
    else:
        print('use caches')

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_7_days'] = get_7_days_hot_blogs()
    return render_to_response('home.html',context)

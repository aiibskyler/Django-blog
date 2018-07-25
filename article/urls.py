from django.urls import path
from . import views


urlpatterns = [

    # localhost:8000/article/1
    path('<int:article_pk>', views.article_detail, name="article_detail"),

    # localhost:8000/article/
    path('', views.article_list, name="article_list"),

    path('type/<int:blog_type_pk>',  views.blog_with_type, name="blog_with_type"),

    path('date/<int:year>/<int:month>', views.articles_with_date, name="articles_with_date"),


]


"""Tdkyq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.static import serve
from django.contrib import admin
from django.urls import path
from django.urls import re_path,include
from django.views.generic import TemplateView
from apps.message_form.views import LoginView,LogoutView
from views import *
from django.conf.urls import url
from Tdkyq.settings import MEDIA_ROOT
from message_form.views import CategoryView,CategoryHomeView,ArticleHomeView,UserHomeView,AddArticleView,UserInfoView,ArticleView

import xadmin

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    path('xadmin/', xadmin.site.urls),

    # path('',TemplateView.as_view(template_name="index.html"),name="index"),
    path('usercenter-info/',UserInfoView.as_view(),name = "usercenter-info"),
    path('article/list', ArticleView.as_view(), name="all_articles"),
    # path('index.html',TemplateView.as_view(template_name="index.html")),
    path('login/', LoginView.as_view(),name="login"),
    path('register.html', RegisterView.as_view(),name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('Category/<int:category>/', CategoryHomeView.as_view(),name = "article_list"),
    path('Category_list/', Category_listView.as_view(),name = "category_list"),
    path('Article/<int:article>/', ArticleHomeView.as_view(), name="comment_list"),
    path('User_Home/<int:author>/', UserHomeView.as_view(), name="user_home"),
    path('add_artiles/<int:category>/', AddArticleView.as_view(), name="add_article"),
    # url(r'^Category/Article/(?P<article>\\d+)/$', ArticleHomeView.as_view(), name='comment_list'),
    url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),
    url(r'',CategoryView.as_view(),name="index"),
    # url(r'^users/', include(('users.urls', "users"), namespace="users")),
    url(r'^message_form/', include(('apps.message_form.urls', "message_form"), namespace="message_form")),
    # url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # url(r'^(?P<category_id>\d+)/$',CategoryHomeView.as_view(),name="category")


]

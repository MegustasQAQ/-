from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate,login,logout
from django.contrib import auth
import login_simulation
from django.forms import forms
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from apps.message_form.models import *
from django.http import JsonResponse
from message_form.forms import ArticlesForm,CommentsForm
from DjangoUeditor.forms import UEditorField
from django.db.models.aggregates import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
#配置一个html页面显示的步骤
#1.配置url
#2.配置对应的views逻辑
#3.拆分静态（css,js,images）放入static,html放入到templates之下
  #（1）可以放到对应的app下面
  #（2）也可以放入到全局的templates和static目录之下
  #（3）配置全局的static文件访问路径的配置STATICFILES_DIRS
# class TestUEditorForm(forms.Form):
#
# content = UEditorField('内容', width=600, height=300, toolbars="full", imagePath="images/", filePath="files/",
#
# upload_settings={"imageMaxSize":1204000},
#
# settings={})


class UserHomeView(View):
    def get(self,request,author,*args,**kwargs):
        user_home = UserProfile.objects.get(username= author)
        all_articles = user_home.article_set.all()
        sort = request.GET.get("sort", "")
        if sort == "click_nums":
            all_articles = all_articles.order_by("-click_nums")
        elif sort == "create_date":
            all_articles = all_articles.order_by("-publish_data")
        elif sort == "comment_nums":
            all_articles = all_articles.order_by("-commment_nums")
        return render(request, "user_article.html", {
            "user_home":user_home,
            'all_articles':all_articles
        })


class ArticleHomeView(View):
    def get(self,request,article,*args,**kwargs):
        comment_article = Article.objects.filter(id = article)
        if comment_article:
            comment_article = comment_article[0]
            comment_article.click_nums += 1
            comment_article.save()
        all_comments = comment_article.comment_set.all()
        return render(request, "Comment.html", {
            "comment_article":comment_article,
            'all_comments':all_comments
        })

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        comemnts_form = CommentsForm(request.POST)


        if comemnts_form.is_valid():
            user = UserProfile(request.user)
            article = comemnts_form.cleaned_data["article"]
            comments = comemnts_form.cleaned_data["comment"]
            article.commment_nums += 1
            article.save()
            user.commment_nums += 1
            comment =  comemnts_form.save(commit=False)
            comment.user = request.user
            comment.comment = comments
            comment.article = article
            comment.save()

            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })

class CategoryHomeView(View):
    def get(self,request,category,*args,**kwargs):
        articles_category = Category.objects.filter(id = category)
        if articles_category:
            articles_category = articles_category[0]
            articles_category.click_nums += 1
            articles_category.save()
        all_articles = articles_category.article_set.all()

        sort = request.GET.get("sort", "")
        if sort == "click_nums":
            all_articles = all_articles.order_by("-click_nums")
        elif sort == "create_date":
            all_articles = all_articles.order_by("-publish_data")
        elif sort == "comment_nums":
            all_articles = all_articles.order_by("-commment_nums")

        return render(request, "Article_list.html", {
            "articles_category":articles_category,
            'all_articles':all_articles,
            'sort':sort
        })



class CategoryView(View):
    def get(self,request,*args,**kwargs):
        all_categories = Category.objects.annotate(num_posts=Count('article'))

        return render(request,"index.html",{
            'all_categories':all_categories,


        })

class Category_listView(View):
    def get(self, request, *args, **kwargs):
        all_categories = Category.objects.annotate(num_posts=Count('article'))
        sort = request.GET.get("sort", "")
        if sort == "click_nums":
            all_categories = all_categories.order_by("-click_nums")
        elif sort == "create_date":
            all_categories = all_categories.order_by("-create_date")
        elif sort == "article_nums":
            all_categories = all_categories.order_by("-articles_nums")
        return render(request, "Category_list.html", {
                'all_categories': all_categories,
                'sort':sort

            })

class RegisterView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"register.html")

    def post(self,request,*args,**kwargs):

            # return render(request,"login.html")
            # login_form = LoginForm(request.POST)
            user_name = request.POST.get("mobile","")
            password = request.POST.get("password","")

            if user_name is None:
                return render(request,"register.html",{"msg":"请输入学号和密码"})
            if password  is None:
                return render(request,"register.html",{"msg":"请输入学号和密码"})

            else:
                name = login_simulation.simulate_login(user_name, password)
                if name is not None:
                    user = UserProfile(username=user_name)
                    user.set_password(password)
                    user.nick_name = name
                    user.save()
                    return render(request, "register.html", {"msg": "注册成功！"})
                else:
                        return render(request, "register.html", {"msg": "该学号不存在或密码错误"})

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

class LoginView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request,"login.html")

    def post(self,request,*args,**kwargs):

            # return render(request,"login.html")
            # login_form = LoginForm(request.POST)
            user_name = request.POST.get("username","")
            password = request.POST.get("password","")

            if not user_name:
                return render(request,"login.html",{"msg":"请输入学号和密码"})
            if not password:
                return render(request,"login.html",{"msg":"请输入学号和密码"})
            if len(user_name) != 12:
                return render(request,"login.html",{"msg":"该学号不存在"})
            # user_name = login_form.cleaned_data["username"]
            # password = login_form.cleaned_data["password"]
            #通过用户名密码查询用户是否存在
            user = authenticate(username=user_name,password=password)
            if user is not None:
                #查询到用户
                auth.login(request,user)
                #登录成功之后返回页面
                return HttpResponseRedirect(reverse("index"))
                # 未查询到用户
            else:

                    return render(request,"login.html",{"msg":"用户名或密码错误"})

class AddArticleView(View):
    def get(self,request,category,*args,**kwargs):
        articles_category = Category.objects.get(id =category)
        return render(request, "add_article.html", {
            "articles_category":articles_category,

        })

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        article_form = ArticlesForm(request.POST)
        if article_form.is_valid():


            category = article_form.cleaned_data["category"]
            # img = article_form.cleaned_data["img"]
            content = article_form.cleaned_data["content"]
            title = article_form.cleaned_data["title"]
            # img = article_form.cleaned_data["img"]

            article = article_form.save(commit=False)
            article.author = request.user
            article.category = category
            article.content = content
            article.title = title
            # article.img = img
            article.save()

            return JsonResponse({
                "status":"success",
                "msg":"发布成功！"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "标题重复或内容错误"
            })

class UploadImageView(View):
    # def get(self, request,  *args, **kwargs):
    #     return render(request, "usercenter-info.html", {
    #     })
    def post(self, request, *args, **kwargs):
        #处理用户上传的头像
        files = request.Files["image"]
        return render(request, "usercenter-info.html", {
            "files":files
        })

class UserInfoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        # current_page = "info"
        # captcha_form = RegisterGetForm()
        return render(request, "usercenter-info.html",{
            # "captcha_form":captcha_form,
            # "current_page":current_page
        })

    def post(self, request, *args, **kwargs):
        # user_info_form = UserInfoForm(request.POST, instance=request.user)
        # if user_info_form.is_valid():
        #     user_info_form.save()
        #     return JsonResponse({
        #         "status":"success"
        #     })
        # else:
         return  JsonResponse({
                "status": "fail",

            })

class ArticleView(View):
    def get(self, request, *args, **kwargs):
        #从数据库中获取数据
        all_articles = Article.objects.all()

        keywords = request.GET.get("keywords", "")
        if keywords:
            all_articles = all_articles.filter(Q(title__icontains=keywords)|Q(content__icontains=keywords)|Q(author__nick_name__icontains=keywords))


        #对机构进行排序
        sort = request.GET.get("sort", "")
        if sort == "click_nums":
            all_articles = all_articles.order_by("-click_nums")
        elif sort == "create_date":
            all_articles = all_articles.order_by("-publish_data")
        elif sort == "comment_nums":
            all_articles = all_articles.order_by("-commment_nums")

        return render(request, "all_articles.html",{
            "all_articles":all_articles,
            "sort":sort,
            "keywords": keywords,
        })

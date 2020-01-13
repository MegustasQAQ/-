from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import admin
from DjangoUeditor.models import UEditorField
from ckeditor_uploader.fields import RichTextUploadingField




# Create your models here.

class Article(models.Model):
    """
    话题表
    """

    title = models.CharField(u"话题标题",max_length=50,unique=True)
    category = models.ForeignKey("Category", verbose_name=u"版块", on_delete=models.CASCADE)
    author = models.ForeignKey("UserProfile", on_delete=models.CASCADE, verbose_name="作者")
    content =UEditorField(u"内容",width=600,height=300,imagePath="Article/ueditor/images",filePath="Article/ueditor/files")
    publish_data = models.DateTimeField(auto_now=True,verbose_name='发布时间')
    hidden = models.BooleanField(default=True)
    commment_nums = models.IntegerField(default=0, verbose_name="评论数")
    click_nums = models.IntegerField(default=0, verbose_name="浏览数")
    user_like_nums = models.IntegerField(default=0, verbose_name ="点赞数")


    class Meta:
        verbose_name = "话题列表"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title

class Category(models.Model):
    """
    版块
    """

    create_date = models.DateTimeField(auto_now=True,verbose_name='创建时间')
    name = models.CharField(max_length=64,unique=True)
    admin = models.ManyToManyField('UserProfile')
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    image = models.ImageField(upload_to="category/%Y/%m", verbose_name="logo", max_length=100)
    articles_nums = models.IntegerField(default=0, verbose_name="文章数")
    desc = UEditorField(verbose_name="描述", width=600, height=300, imagePath="categories/ueditor/images/",
                        filePath="categories/ueditor/files/", default="")
    class Meta:
        verbose_name = "版块列表"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Comment(models.Model):
    """
    存储所有评论
    """
    article = models.ForeignKey("Article",on_delete=models.CASCADE,verbose_name="话题")
    user = models.ForeignKey("UserProfile",on_delete=models.CASCADE,verbose_name="评论者")
    # parent_comment = models.ForeignKey('self',related_name='p_comment',blank=True,null=True,on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000,verbose_name="评论内容")
    date= models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name = "评论列表"
        verbose_name_plural = verbose_name
    def __str__(self):
       return self.comment


class User_like(models.Model):
    """
    点赞
    """
    article = models.ForeignKey('Article',on_delete=models.CASCADE)
    user = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add = True)
    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.user





GENDER_CHOICES = (
    ("male", "男"),
    ("female", "女")
)


class UserProfile(AbstractUser):
    """
    账户信息表                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                w
    """
    articles_nums = models.IntegerField(default=0, verbose_name="文章数")
    commment_nums = models.IntegerField(default=0, verbose_name="评论数")
    idiograph = models.CharField(max_length=64,verbose_name="个人签名",default="")
    city = models.CharField(max_length=16,verbose_name="城市",default="")
    nick_name = models.CharField(max_length=50,verbose_name='昵称',default="")
    birthday = models.DateField(verbose_name="生日",null=True,blank=True)
    #gender = models.CharField(verbose_name='性别',choices=GENDER_CHOICES,max_length=6)
    mobile = models.CharField(max_length=11,verbose_name="联系方式")
    image = models.ImageField(verbose_name="用户头像", upload_to="head_image/%Y/%m", default="head_image/2019/12/default.jpg")
    #user = models.OneToOneField(AbstractUser,on_delete=models.CASCADE)
    #name = models.CharField(max_length=32)
    # groups = models.ManyToManyField("UserGroup")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username






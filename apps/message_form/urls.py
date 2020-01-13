from django.conf.urls import url
from django.views.generic import TemplateView
from views import UploadImageView
from django.urls import re_path,include
from django.urls import path

urlpatterns = [


    path('message_form/image/upload/',UploadImageView.as_view(),name = "image"),

]

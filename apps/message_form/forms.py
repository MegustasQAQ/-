from django import forms
from apps.message_form.models import *

class LoginForm(forms.Form):
    user_name = forms.CharField(required=True,min_length=12,max_length=12)
    password = forms.CharField(required=True,min_length=3)

class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["category","title","content"]

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["article","comment"]

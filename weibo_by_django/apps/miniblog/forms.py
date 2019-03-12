# _*_ coding:utf-8 _*_

from django import forms
from captcha.fields import CaptchaField
from .models import MiniBlog


class BlogContentForm(forms.Form):
    content = forms.CharField(required=True, max_length=500)
    image = forms.FileField(required=False)
    # class Meta:
    #     model = MiniBlog
    #     fields = ['user',"content", "image"]


class SearchContentForm(forms.Form):
    searchtext = forms.CharField(required=True, max_length=50)
    searchtype = forms.CharField(required=True)

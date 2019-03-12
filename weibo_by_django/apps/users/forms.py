# _*_ coding:utf-8 _*_

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


# 登录表单验证
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


# 注册表单+验证码,返回register_form的html才有验证码
class RegisterForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': "验证码输入错误"})


class FindPwdForm(forms.Form):
    email = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid': "验证码输入错误"})


class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

#
# class MainPageLoginForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ["username", "password"]

class MainPageLoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=5)

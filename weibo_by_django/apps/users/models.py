# _*_ coding: utf-8 _*_

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# 描述用户信息,继承的是内置的auth_user类
class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=30, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), max_length=10, verbose_name="性别",
                              default='female')
    address = models.CharField(max_length=200, verbose_name="地址", default='')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机")
    image = models.ImageField(upload_to="UserProfile/%Y/%m", default="image/default.png", max_length=100, verbose_name="头像")
    fans_num = models.IntegerField(verbose_name="粉丝数", default=0)
    blog_num = models.IntegerField(verbose_name="微博数", default=0)
    follow_num = models.IntegerField(verbose_name="关注数", default=0)
    add_time = models.DateField(default=datetime.now, verbose_name="加入时间")

    message_nums = models.IntegerField(verbose_name='未读消息数', default=0)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 邮箱验证码类
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="邮箱验证码")
    email = models.CharField(max_length=40, verbose_name="邮箱")
    send_type = models.CharField(choices=(("register", "注册"), ("findback", "找回密码")), max_length=20)
    send_time = models.DateField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}({1})".format(self.code, self.email)


# 未登录页轮播图
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    index = models.IntegerField(default=1000, verbose_name="播放顺序")
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name="轮播图", max_length=100)
    jmp_url = models.URLField(max_length=200, verbose_name="跳转地址")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

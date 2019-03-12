# _*_ coding: utf-8 _*_

from django.db import models
from datetime import datetime

from users.models import UserProfile


# Create your models here.

class Topic(models.Model):
    topicname = models.CharField(default="", max_length=50, verbose_name="话题名称")
    aboutblogs_num = models.IntegerField(verbose_name="相关微博数", default=0, null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        verbose_name = "微博话题"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.topicname[:10]


class MiniBlog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="发布用戶", null=True, blank=True,
                             related_name='miniblog_set')
    content = models.TextField(verbose_name="微博正文")
    image = models.ImageField(upload_to="blogImage/%Y/%m", verbose_name="图片", null=True, blank=True, max_length=200)
    click_num = models.IntegerField(verbose_name="微博点击数", default=0, null=True, blank=True)
    good_num = models.IntegerField(verbose_name="点赞数", default=0, null=True, blank=True)
    comment_num = models.IntegerField(verbose_name="评论数", default=0, null=True, blank=True)
    collect_num = models.IntegerField(verbose_name="收藏数", default=0, null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="发布时间")
    has_pic = models.IntegerField(verbose_name="是否有图", default=0, null=True, blank=True)

    need_unfold = models.IntegerField(choices=((0, "不需展开"), (1, "需要展开且未展开"), (2, "需展开且已展开")), default=0)

    related_topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True, verbose_name="微博相关话题")

    class Meta:
        verbose_name = "微博"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content[:10]

    def shorttext(self):
        return self.content[:10] + "..."

    def judgefold(self):
        foldlen = 5
        if len(self.content) < foldlen:
            self.need_unfold = 0  # 不需展开
        else:
            self.need_unfold = 1

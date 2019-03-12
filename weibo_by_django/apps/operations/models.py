from django.db import models
from datetime import datetime

from miniblog.models import MiniBlog
from users.models import UserProfile


# Create your models here.

# 用户点赞
class UserGood(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True, verbose_name="点赞用户")
    blog = models.ForeignKey(MiniBlog, on_delete=models.CASCADE, blank=True, null=True, verbose_name="被点赞微博")
    # blogid = models.IntegerField(default=0, verbose_name="微博id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="点赞时间")

    class Meta:
        verbose_name = "用户点赞"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}->blog_id{1}".format(self.user.username, self.blog_id)


# 用户收藏
class UserFav(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name="收藏用户")
    blog = models.ForeignKey(MiniBlog, on_delete=models.CASCADE, blank=True, null=True, verbose_name="被收藏微博")
    # blogid = models.IntegerField(default=0, verbose_name="微博id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}->blog_id{1}".format(self.user.username, self.blog_id)


# 用户关注,给每个被关注的用户家外键指向关注其的用户
# 认为被关注人从属于发起关注的人，类似于微博和用户的关系
# 使用userfollowed_set得到所有关注的人，用fans_set得到所有的粉丝
class UserFollowed(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name="被关注的用户",
                             related_name='fans_set')
    follow_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name="关注其的用户")
    followUser_id = models.IntegerField(default=0, verbose_name="被关注用户id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="关注时间")

    class Meta:
        verbose_name = "用户关注"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}->id{1}".format(self.user.username, self.followUser_id)


class UserMessage(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name="接收用户")
    # userid = models.IntegerField(default=0, verbose_name="用户id")
    message = models.CharField(max_length=500, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    blog_id = models.IntegerField(default=0, verbose_name='微博id')

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "id{0}:{1}".format(self.user_id, self.message[:5])


# 博客评论（L）
class BlogComment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
    blog = models.ForeignKey(MiniBlog, verbose_name=u'微博', on_delete=models.CASCADE)# __str__ returned non-string (type UserProfile)
    reply_user = models.ForeignKey(UserProfile, verbose_name=u'评论的人', on_delete=models.CASCADE, null=True, blank=True, related_name='reply_user')
    comment = models.CharField(max_length=100, verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'评论'
        verbose_name_plural = verbose_name

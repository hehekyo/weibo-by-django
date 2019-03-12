# _*_ coding:utf-8 _*_

from django.contrib import admin
from django.urls import path, include
import xadmin
from django.views.generic import TemplateView

from users.views import user_login, LoginView, RegisterView, ActivateView, FindbackPwd, ResetPwdView, ModifyPwdView
from miniblog.views import MainpageView, SendBlogView, DelBlogView, CollectBlogView, TransferBlogView, CommentBlogView, \
    GoodBlogView, BlogTextPageView, SearchView, EditBLogView,TopicView, AddCommentView

# weibo/xxxx
# app_name = 'miniblog'
urlpatterns = [

    # 发布微博
    path('sendblog/', SendBlogView.as_view(), name='sendblog'),

    # 删除
    path('delblog/<int:blog_id>', DelBlogView.as_view(), name='delblog'),

    # 跳到对应微博正文+评论页面
    path('blogtext/<int:blog_id>', BlogTextPageView.as_view(), name="blogtext"),

    path('collect/<int:blogid>', CollectBlogView.as_view(), name='collect'),
    path('transfer/<int:blogid>', TransferBlogView.as_view(), name='transfer'),
    path('comment/<int:blogid>', CommentBlogView.as_view(), name='comment'),
    path('good/<int:blogid>', GoodBlogView.as_view(), name='good'),
    path('search/', SearchView.as_view(), name='search'),




    path('edit/<int:blogid>', EditBLogView.as_view(), name="editblog"),
    path('topic/<int:topicid>', TopicView.as_view(), name="topic"),

    # 添加一条评论（新增）
    path('add_comment/<int:blog_id>', AddCommentView.as_view(), name='add_comment'),
]

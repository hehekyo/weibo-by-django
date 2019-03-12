# _*_ coding:utf-8 _*_

from django.conf.urls import url
from django.urls import path

from .views import AddFollowView, MessageView, UserFollowView, UserFansView, UserInfoView, PwdView, ImageView

app_name = 'operation'

urlpatterns = [
    # 添加关注
    path('add_follow/', AddFollowView.as_view(), name='add_follow'),
    # 用户消息页面
    path('message/', MessageView.as_view(), name='message'),
    # 关注页面
    path('user_follow/<int:userid>', UserFollowView.as_view(), name='user_follow'),
    # 粉丝页面
    path('user_fans/<int:userid>', UserFansView.as_view(), name='user_fans'),
    # 用户信息页面
    path('info/', UserInfoView.as_view(), name='user_info'),
    # 修改密码
    path('pwd/', PwdView.as_view(), name='pwd'),
    path('image/', ImageView.as_view(), name='image')
    # # 添加关注
    # url(r'^add_follow/$', AddFollowView.as_view(), name='add_follow'),
    # # 关注页面
    # url(r'^user_follow/$', UserFollowView.as_view(), name='user_follow'),
    # # 粉丝页面
    # url(r'^user_fans/$', UserFansView.as_view(), name='user_fans'),
]

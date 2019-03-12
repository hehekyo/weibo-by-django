# _*_ coding:utf-8 _*_

import xadmin

from .models import UserGood, UserFav, UserFollowed, UserMessage


# 设置MiniBlog在界面中的显示
class UserGoodAdmin(object):
    list_display = ['user', 'blog', 'add_time']
    search_fields = ['user', 'blog']
    list_filter = ['user', 'blog', 'add_time']


class UserFavAdmin(object):
    list_display = ['user', 'blog', 'add_time']
    search_fields = ['user', 'blog']
    list_filter = ['user', 'blog', 'add_time']


class UserFollowedAdmin(object):
    list_display = ['user', 'follow_user', 'add_time']
    search_fields = ['user', 'follow_user']
    list_filter = ['user', 'follow_user', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


# 注册model
xadmin.site.register(UserGood, UserGoodAdmin)
xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserFollowed, UserFollowedAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)

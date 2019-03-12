# _*_ coding: utf-8 _*_

import xadmin

from .models import MiniBlog,Topic


# 设置MiniBlog在界面中的显示
class MiniBlogAdmin(object):
    list_display = ['user', 'content', 'image', 'click_num', 'good_num', 'comment_num', 'add_time']
    search_fields = ['user', 'content', 'image', 'click_num', 'good_num', 'comment_num']
    list_filter = ['user', 'content', 'image', 'click_num', 'good_num', 'comment_num', 'add_time']


class TopicAdmin(object):
    list_display = ['topicname','add_time']
    search_fields = ['topicname']
    list_filter = ['topicname','add_time']


# 注册model
xadmin.site.register(MiniBlog, MiniBlogAdmin)
xadmin.site.register(Topic, TopicAdmin)

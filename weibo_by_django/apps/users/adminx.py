# _*_ coding utf-8 _*_

import xadmin
from xadmin import views

from .models import UserProfile, EmailVerifyRecord, Banner


# 修改主题
class BaseSetting(object):
    enable_themes = True  # 能使用自定义主题
    use_bootswatch = True


# 修改后台布局
class GlobalSetting(object):
    site_title = "微博后台管理系统"
    site_footer = "我的微博"
    menu_style = "accordion"


# UserProfile django已经注册

# class UserProFileAdmin(object):
#     list_display = ['nickname', 'gender', 'image', 'fans_num', 'blog_num', 'follow_num', 'add_time']
#     search_fields = ['nickname', 'gender', 'image', 'fans_num', 'blog_num', 'follow_num']
#     list_filter = ['nickname', 'gender', 'image', 'fans_num', 'blog_num', 'follow_num', 'add_time']


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'index', 'add_time', 'image', 'jmp_url']
    search_fields = ['title', 'index', 'image', 'jmp_url']
    list_filter = ['title', 'index', 'add_time', 'image', 'jmp_url']


# xadmin.site.register(UserProfile, UserProFileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)

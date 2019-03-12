# _*_ coding:utf-8 _*_

from django.urls import path, include

from users.views import user_login, UserPageView, MyCollectView,MyGoodView

urlpatterns = [

    # 跳到用户主页路由
    path('<int:user_id>/', UserPageView.as_view(), name="userpage"),

    path('mycollect/', MyCollectView.as_view(), name="mycollect"),
    path('mygood/', MyGoodView.as_view(), name="mygood"),
]

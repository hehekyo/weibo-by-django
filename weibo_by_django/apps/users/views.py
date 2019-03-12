# _*_ coding utf-8 _*_

from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from itertools import chain

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, FindPwdForm, ResetPwdForm, MainPageLoginForm
from util.send_email import send_veri_email
from operations.models import UserFav, UserGood
from miniblog.models import MiniBlog, Topic
from operations.models import UserFollowed


# Create your views here.


# 后台自定义验证authenticate,邮箱，用户名都能验证
class CustomBackend(ModelBackend):
    # 重写authenticate方法
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # get的前一个username对应UserProfile类中的属性
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # 得到一个对应的用户进行密码验证
            if user.check_password(password):
                return user

        except Exception as e:
            return None


def user_login(request):
    if request.method == 'GET':
        return render(request, 'Login.html', {})
    elif request.method == 'POST':
        user_name = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # authenticate有两个默认参数username,password
        user = authenticate(username=user_name, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'MainPage.html', {})
        else:
            return render(request, 'Login.html', {'errmsg': "用户名/密码错误"})


# 处理登录
class LoginView(View):
    # 重写get方法，处理以get方式提交的分支
    def get(self, request):
        return render(request, 'Login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            password = request.POST.get('password', '')
            # authenticate有两个默认参数username,password
            user = authenticate(username=user_name, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('mainpage'))
                else:
                    return render(request, "Login.html", {'errmsg': "用户未激活"})
            else:
                return render(request, 'Login.html', {'errmsg': "用户名/密码错误"})
        else:
            return render(request, 'Login.html', {'errmsg': "用户名/密码错误", 'login_form': login_form})

#注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm();
        return render(request, "Register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_email):
                return render(request, "Register.html", {'errmsg': "该邮箱已被注册", 'register_form': register_form})
            user_password = request.POST.get("password", "")
            userReg = UserProfile()
            userReg.is_active = False
            userReg.username = user_email
            userReg.email = user_email
            userReg.password = make_password(user_password)
            userReg.save()
            send_veri_email(user_email, "register")
            return render(request, "SendEmailActivate.html")
        else:
            return render(request, "Register.html", {"register_form": register_form})


# 点击链接激活后直接跳转到登录页面登录
class ActivateView(View):
    def get(self, request, act_code):
        all_records = EmailVerifyRecord.objects.filter(code=act_code)
        # 若找到对应的code
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, "Login.html")
        else:
            return render(request, "Activate_fail.html")


# 点击忘记密码进入到提交邮箱验证码页面
class FindbackPwd(View):
    def get(self, request):
        find_form = FindPwdForm()
        return render(request, "Password_findback.html", {'find_form': find_form})
    def post(self, request):
        find_form = FindPwdForm(request.POST)
        if find_form.is_valid():
            user_email = request.POST.get("email", "")
            user = UserProfile.objects.filter(email=user_email)
            if user:
                send_veri_email(user_email, "findback")
                return render(request, "SendEmailResetPwd.html")
            else:
                return render(request, "Password_findback.html", {'errmsg': "该邮箱账号未注册", 'find_form': find_form})


# 进入到重置密码页面
class ResetPwdView(View):
    def get(self, request, res_code):
        all_records = EmailVerifyRecord.objects.filter(code=res_code)
        # 若找到对应的code的所有对象
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "Password_reset.html", {'email': email})
        else:
            return render(request, "Activate_fail.html")
        return render(request, "Login.html")


# 提交重置密码
class ModifyPwdView(View):
    def post(self, request):
        resetpwd_form = ResetPwdForm(request.POST)
        email = request.POST.get("email")
        if resetpwd_form.is_valid():
            pwd1 = request.POST.get("password1")
            pwd2 = request.POST.get("password2")

            if pwd1 != pwd2:
                return render(request, "Password_reset.html", {"errmsg": "输入的密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, "Login.html")
        else:
            return render(request, "Password_reset.html", {'resetpwd_form': resetpwd_form})


# 跳转用户主页处理
class UserPageView(View):
    def get(self, request, user_id):
        has_follow = False
        if request.user.is_authenticated:
            exist_record = UserFollowed.objects.filter(user_id=int(user_id), follow_user=request.user)
            if exist_record:
                has_follow = True

            sort = request.GET.get("sort", "")
            if sort == 'time':
                user = UserProfile.objects.get(id=user_id)
                all_blogs = user.miniblog_set.all().order_by('-add_time')
            elif sort == 'hot':
                user = UserProfile.objects.get(id=user_id)
                all_blogs = user.miniblog_set.all().order_by('-click_num')
            elif sort == 'comment':
                user = UserProfile.objects.get(id=user_id)
                all_blogs = user.miniblog_set.all().order_by('-comment_num')
            else:
                user = UserProfile.objects.get(id=user_id)
                all_blogs = user.miniblog_set.all().order_by('-add_time')
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            p = Paginator(all_blogs, 3, request=request)
            user_blogs = p.page(page)
            return render(request, "UserPage.html",
                          {'user': user, 'user_blogs': user_blogs, 'sort': sort, 'has_follow': has_follow})

        else:
            return HttpResponseRedirect('/')


# 主页中的登陆处理
class MainPageLoginView(View):
    def post(self, request):
        user_form = MainPageLoginForm(request.POST)
        if user_form.is_valid():
            # user = user_form.save(commit=True)
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse({"status": "success"})
                else:
                    return JsonResponse({"status": "fail", "msg": "用户未激活"})
            else:
                return JsonResponse({"status": "fail", "msg": "用户名/密码错误"})
        else:
            return JsonResponse({"status": "fail", "msg": "输入不合法"})
            # return JsonResponse({"status": "success"})


# 显示我的收藏页面
class MyCollectView(View):
    def get(self, request):
        if request.user.is_authenticated:

            all_favusers = UserFav.objects.filter(user=request.user).order_by('-add_time')

            the_blogs = [favuser.blog for favuser in all_favusers]
            # 将list转化为queryset
            all_blogs = MiniBlog.objects.filter(pk__in=[x.pk for x in the_blogs])
            all_blogs = all_blogs.order_by('-add_time')

            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            p = Paginator(all_blogs, 3, request=request)
            user_blogs = p.page(page)
            return render(request, "MyCollect.html", {'user': request.user, 'user_blogs': user_blogs})

        else:
            return HttpResponseRedirect('/')


class MyGoodView(View):
    def get(self, request):
        if request.user.is_authenticated:

            all_good = UserGood.objects.filter(user=request.user)
            the_blogs = [good.blog for good in all_good]
            all_blogs = MiniBlog.objects.filter(pk__in=[x.pk for x in the_blogs])

            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            p = Paginator(all_blogs, 3, request=request)
            user_blogs = p.page(page)
            return render(request, "MyGood.html", {'user': request.user, 'user_blogs': user_blogs})

        else:
            return HttpResponseRedirect('/')


class HotBlogView(View):
    def get(self, request):
        all_blogs = MiniBlog.objects.all().order_by('-click_num')[:10]

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blogs, 3, request=request)
        user_blogs = p.page(page)
        all_topic = Topic.objects.all().order_by('-aboutblogs_num')[:10]
        return render(request, "HotBlogAll.html", {'blogs': user_blogs, 'all_topic': all_topic})


# （新增）
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))

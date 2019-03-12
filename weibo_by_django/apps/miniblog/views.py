import re

from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login
from itertools import chain

# Create your views here.
from django.views.generic.base import View
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import MiniBlog, Topic
from operations.models import BlogComment
from users.models import UserProfile
from operations.models import UserFollowed, UserFav, UserGood, UserMessage
from .forms import BlogContentForm, SearchContentForm


# 当用户登录时，返回其关注的人的微博，没登录返回所有微博
class MainpageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            # 要合并所有关注人的微博
            all_favusers = UserFollowed.objects.filter(follow_user=request.user)
            all_user = [favuser.user for favuser in all_favusers]
            all_blogs = MiniBlog.objects.filter(Q(user__in=all_user) | Q(user=request.user)).order_by('-add_time')
            # user_blog = MiniBlog.objects.filter(user=request.user)

            sort = request.GET.get("sort", "")
            if sort == 'time':
                all_blogs = all_blogs.order_by('-add_time')
            elif sort == 'hot':
                all_blogs = all_blogs.order_by('-click_num')
            elif sort == 'comment':
                all_blogs = all_blogs.order_by('-comment_num')
            else:
                all_blogs = all_blogs.order_by('-add_time')


        # all_blogs = request.user.miniblog_set.all()
        else:
            all_blogs = MiniBlog.objects.all().order_by('-add_time')

        # 进行分页传递
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_blogs, 3, request=request)
        blogs = p.page(page)

        all_topic = Topic.objects.all().order_by('-aboutblogs_num')[:10]
        if request.user.is_authenticated:
            return render(request, 'MainPage.html', {'blogs': blogs, 'all_topic': all_topic, 'sort': sort})
        else:
            return render(request, 'MainPage.html', {'blogs': blogs, 'all_topic': all_topic})


# 跳转到单篇微博的页面
class BlogTextPageView(View):
    def get(self, request, blog_id):
        # 点击量加一
        # blog = MiniBlog.objects.get(id=blog_id)
        blog = MiniBlog.objects.get(id=int(blog_id))
        blog.click_num += 1
        blog.save()
        # return HttpResponse("to be continued for your work微博+评论区")
        # （新增）
        comments = BlogComment.objects.filter(blog=blog)
        return render(request, 'blog_detail.html', {
            'blog': blog,
            'comments': comments
        })
        # return render(request, 'Activate_fail.html', {
        #     'blog': blog,
        #     'comments': comments
        # })


# 发布微博  发送微博的url，url=weibo/sendblog, 检测是否有图，检测是否有话题
class SendBlogView(View):
    def post(self, request):
        blog_form = BlogContentForm(request.POST, request.FILES or None)
        if blog_form.is_valid():
            blog = MiniBlog()
            print(blog.id)
            blog.user = request.user
            blog.content = request.POST.get("content", "")
            blog.image = blog_form.cleaned_data["image"]
            if blog.image:
                blog.has_pic = 1

            # 替换@用户
            re_str = blog.content
            users_list = []
            users_str = re.findall(r'@(.+?)\s', re_str)

            users_str_1 = re.findall(r'^(.+?)@', re_str[::-1])
            if users_str_1:
                users_str.append(users_str_1[0][::-1])

            for user_str in users_str:
                user = UserProfile.objects.filter(nickname=user_str)
                if user:
                    users_list.append(user[0])
                    re_str = re_str.replace('@' + user_str,
                                            '<a href="/user/' + str(user[0].id) + '/">' + '@' + user_str + '</a>')
            blog.content = re_str

            blog.save()
            print(blog.id)

            # 新建@提醒
            for user in users_list:
                message = UserMessage()
                message.user = user
                message.blog_id = blog.id
                message.save()

                user.message_nums = UserMessage.objects.filter(user=user, has_read=False).count()
                user.save()

            # blog_form.save()
            self.topic_test(blog.content, blog)

            # 替换话题
            re_str = blog.content
            topics_str = re.findall(r'#(.+?)#', re_str)
            for topic_str in topics_str:
                topic = Topic.objects.filter(topicname=topic_str)
                if topic:
                    re_str = re_str.replace('#' + topic_str + '#', '<a href="/weibo/topic/' + str(
                        topic[0].id) + '">' + '#' + topic_str + '#' + '</a>')

            blog.content = re_str
            blog.save()
            return HttpResponseRedirect(reverse('mainpage'))
        # else:
        #     return JsonResponse({"status": "fail", "msg": "微博不符要求，不能发布"})

    def topic_test(self, content, blog):
        is_topic = 0
        strlist = list(content)
        for index, word in enumerate(strlist):
            if word == "#" and is_topic == 0:
                is_topic = 1
                startindex = index
            elif word == '#' and is_topic == 1:
                is_topic = 0
                endindex = index
                topiclist = strlist[startindex + 1:endindex]
                topic = Topic()
                topic.topicname = ''.join(topiclist)
                se_topic = Topic.objects.filter(topicname=topic.topicname)
                if not se_topic:
                    topic.aboutblogs_num = 1
                    topic.save()
                    blog.related_topic = topic
                else:
                    se_topic = Topic.objects.get(topicname=topic.topicname)
                    se_topic.aboutblogs_num += 1
                    se_topic.save()
                    blog.related_topic_id = se_topic
                blog.save()


# 删除对应微博
class DelBlogView(View):
    def get(self, request, blog_id):
        request.user.blog_num -= 1
        request.user.save()
        MiniBlog.objects.filter(id=blog_id).delete()
        all_blogs = MiniBlog.objects.filter(user=request.user).order_by('-add_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blogs, 3, request=request)
        user_blogs = p.page(page)
        # redirect跳转的格式
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        # return HttpResponseRedirect(reverse("user:userpage", args=(request.user.id,)))
        # return render(request, "UserPage.html", {'user': request.user, 'user_blogs': user_blogs})


# 在主页点击已收藏
class CollectBlogView(View):
    def get(self, request, blogid):
        blog = MiniBlog.objects.get(id=blogid)
        record = UserFav.objects.filter(user=request.user, blog=blog)
        # 若记录为空则添加，否则删除,判空不用None
        if record:
            record.delete()
            blog.collect_num -= 1
            blog.click_num += 1
            blog.save()
        else:
            userfav = UserFav()
            userfav.user = request.user
            userfav.blog = blog
            blog.collect_num += 1
            blog.click_num += 1
            blog.save()
            userfav.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#点赞
class GoodBlogView(View):
    def get(self, request, blogid):
        blog = MiniBlog.objects.get(id=blogid)
        record = UserGood.objects.filter(user=request.user, blog=blog)
        # 若记录为空则添加，否则删除,判空不用None
        if record:
            record.delete()
            blog.good_num -= 1
            blog.click_num += 1
            blog.save()
        else:
            usergood = UserGood()
            usergood.user = request.user
            usergood.blog = blog
            blog.good_num += 1
            blog.click_num += 1
            blog.save()
            usergood.save()
        source_ad = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(source_ad)


# 搜索，三种搜索模式:话题，全部微博，自己的微博
class SearchView(View):
    def post(self, request):
        search_form = SearchContentForm(request.POST)
        if search_form.is_valid():
            searchtext = request.POST.get("searchtext", "")
            search_type = request.POST.get("searchtype", "")
            if search_type == "topic":
                all_topic = Topic.objects.filter(Q(miniblog__content__contains=searchtext))
                try:
                    page = request.GET.get('page', 1)
                except PageNotAnInteger:
                    page = 1
                p = Paginator(all_topic, 3, request=request)
                all_topic = p.page(page)

                rank_topic = Topic.objects.all().order_by('-aboutblogs_num')
                return render(request, "TopicSearch.html", {'search_topic': all_topic, 'all_topic': rank_topic})

            elif search_type == "allblogs":
                all_blogs = MiniBlog.objects.filter(
                    Q(content__contains=searchtext) | Q(user__nickname__contains=searchtext) | Q(
                        user__username__contains=searchtext) | Q(user__email__contains=searchtext) | Q(
                        user__address__contains=searchtext) | Q(user__gender__contains=searchtext) | Q(
                        user__mobile__contains=searchtext))
                try:
                    page = request.GET.get('page', 1)
                except PageNotAnInteger:
                    page = 1
                p = Paginator(all_blogs, 3, request=request)
                user_blogs = p.page(page)
                all_topic = Topic.objects.all().order_by('-aboutblogs_num')[:10]
                return render(request, 'MainSePage.html', {'blogs': user_blogs, 'all_topic': all_topic})

            elif search_type == "myblogs":
                my_blog = MiniBlog.objects.filter(user=request.user)

                all_blogs = my_blog.filter((Q(content__contains=searchtext) | Q(
                    user__nickname__contains=searchtext) | Q(
                    user__username__contains=searchtext) | Q(user__email__contains=searchtext) | Q(
                    user__address__contains=searchtext) | Q(user__gender__contains=searchtext) | Q(
                    user__mobile__contains=searchtext))).order_by("-add_time")
                try:
                    page = request.GET.get('page', 1)
                except PageNotAnInteger:
                    page = 1
                p = Paginator(all_blogs, 3, request=request)
                user_blogs = p.page(page)
                return render(request, "UserSePage.html",
                              {'user': request.user, 'user_blogs': user_blogs, 'sort': "time"})
        else:
            return JsonResponse({"status": "fail", "msg": "微博不符要求，不能发布"})

    def get(self, request):
        # return HttpResponseRedirect(reverse('user:userpage', args=(request.user.id,)))
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return HttpResponseRedirect(reverse('mainpage'))


class TransferBlogView(View):
    def get(self, request, blogid):
        return HttpResponse("跳转到转发微博页面，在该页面点击发布即可转发")


class CommentBlogView(View):
    def get(self, request, blogid):
        return HttpResponse("应跳转到对应的微博页面进行评论")

#编辑微博
class EditBLogView(View):
    def get(self, request, blogid):
        blog = MiniBlog.objects.get(id=blogid)
        return render(request, "EditBlog.html", {'blog': blog})

    def post(self, request, blogid):
        blog_form = BlogContentForm(request.POST, request.FILES or None)
        edit_blog = MiniBlog.objects.get(id=blogid)
        if blog_form.is_valid():
            # blog = MiniBlog()
            # blog.user = request.user
            edit_blog.content = request.POST.get("content", "")
            if blog_form.cleaned_data["image"]:
                edit_blog.image = blog_form.cleaned_data["image"]
            if edit_blog.image:
                edit_blog.has_pic = 1

            edit_blog.save()
            # blog_form.save()
            SendBlogView.topic_test(SendBlogView(), edit_blog.content, edit_blog)
            return HttpResponseRedirect(reverse('mainpage'))


# 返回话题相关的所有微博
class TopicView(View):
    def get(self, request, topicid):
        the_topic = Topic.objects.get(id=topicid)
        topic_blog = MiniBlog.objects.filter(related_topic=the_topic).order_by('-click_num')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(topic_blog, 3, request=request)
        blogs = p.page(page)

        all_topic = Topic.objects.all().order_by('-aboutblogs_num')[:10]
        return render(request, 'TopicBlogShow.html', {'blogs': blogs, 'all_topic': all_topic, 'the_topic': the_topic})


# 添加一条评论（新增）
class AddCommentView(View):
    def post(self, request, blog_id):
        the_blog = MiniBlog.objects.get(id=blog_id)
        the_blog.comment_num += 1
        the_blog.save()
        comment = BlogComment()
        comment.user = request.user
        comment.blog_id = blog_id
        comment.comment = request.POST.get('blog_text', '')

        reply_user_id = request.POST.get('user_id', '0')
        if int(reply_user_id) != 0:
            comment.reply_user_id = reply_user_id

        comment.save()
        return redirect(reverse('weibo:blogtext', kwargs={
            'blog_id': int(blog_id)
        }))

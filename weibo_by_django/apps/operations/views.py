from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.http import JsonResponse

from .models import UserFollowed
from users.models import UserProfile
from miniblog.models import MiniBlog
from .models import UserMessage
from django.contrib.auth.hashers import check_password, make_password


class AddFollowView(View):
    def post(self, request):
        follow_id = request.POST.get('followed_id', 0)
        if int(follow_id) <= 0:  # 错误
            return JsonResponse({'status': 'fail'})
        else:
            follow_user = UserProfile.objects.get(pk=int(follow_id))
            exist_record = UserFollowed.objects.filter(user=follow_user, follow_user=request.user)

            json_dict = {}
            if exist_record:
                # 已关注，用户取消关注
                exist_record.delete()
                json_dict = {'status': 'success', 'msg': '关注'}
            else:
                # 添加新纪录
                follow = UserFollowed()
                follow.user = follow_user
                follow.follow_user = request.user
                follow.save()
                json_dict = {'status': 'success', 'msg': '已关注'}

            # 更新粉丝数
            request.user.follow_num = UserFollowed.objects.filter(follow_user=request.user).count()
            request.user.save()
            # 更新关注数
            follow_user.fans_num = UserFollowed.objects.filter().count()
            follow_user.save()

            return JsonResponse(json_dict)


class MessageView(View):
    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        # messages = UserMessage.objects.filter(user=user, has_read=False)
        messages = UserMessage.objects.filter(user=user)
        blog_ids = [message.blog_id for message in messages]
        blogs = MiniBlog.objects.filter(id__in=blog_ids)
        for message in messages:
            message.has_read = True
            message.save()
        user.message_nums = UserMessage.objects.filter(user=user, has_read=False).count()
        user.save()
        return render(request, 'MessagePage.html', {
            'blogs': blogs
        })


class UserFollowView(View):
    def get(self, request, userid):
        follows = UserFollowed.objects.filter(follow_user_id=userid)
        user = UserProfile.objects.get(id=userid)
        return render(request, 'user_follow.html', {
            'follows': follows,
            'user': user
        })


class UserFansView(View):
    def get(self, request, userid):
        follows = UserFollowed.objects.filter(user_id=userid)
        user = UserProfile.objects.get(id=userid)
        return render(request, 'user_fans.html', {
            'follows': follows,
            'user': user
        })


class UserInfoView(View):
    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        return render(request, 'UserInfo.html', {
            'user': user
        })

    def post(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        nickname = request.POST['nickname']
        exist_record = UserProfile.objects.filter(nickname=nickname)
        if exist_record and exist_record[0] != user:
            return render(request, 'UserInfo.html', {
                'user': user,
                'msg': '昵称已被使用'
            })
        else:
            user.nickname = nickname
            user.address = request.POST['address']
            user.mobile = request.POST['mobile']
            user.save()
            return render(request, 'UserInfo.html', {
                'user': user,
                'msg': '修改成功'
            })


class PwdView(View):
    def post(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        old = request.POST['password1']
        new = request.POST['password2']
        if not check_password(old, user.password):
            return render(request, 'UserInfo.html', {
                'user': user,
                'msg_pwd': '旧密码不正确'
            })
        if len(new) < 6:
            return render(request, 'UserInfo.html', {
                'user': user,
                'msg_pwd': '新密码小于6位'
            })
        else:
            user.password = make_password(new)
            user.save()
            redirect(reverse('login'))


class ImageView(View):
    def post(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        user.image = request.FILES.get("image", "")
        if user.image:
            user.save()
        return render(request, 'UserInfo.html', {
            'user': user
        })

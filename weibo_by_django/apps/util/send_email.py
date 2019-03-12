# _*_ coding:utf-8 _*_

from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from weibo.settings import EMAIL_FROM


# 随机生成指定长度字符串
def generate_code(randomLen=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    totalLen = len(chars) - 1
    random = Random()
    for i in range(randomLen):
        str += chars[random.randint(0, totalLen)]
    return str


# 发送邮件链接，传入的参数email是邮件地址
def send_veri_email(email, send_type="register"):
    # 记录已发送的邮件
    email_record = EmailVerifyRecord()
    code = generate_code(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    if send_type == 'register':
        email_title = "微博认证信息"
        email_body = "请点击下面的连接激活你的账户 http://127.0.0.1:8000/activate/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'findback':
        email_title = "微博找回密码链接"
        email_body = "请点击下面的链接重置密码 http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

from django.urls import re_path, path

from verify_code.views import SendSmsCode, CheckSmsCode, SendEmailCode, CheckEmailCode



urlpatterns = [
    re_path(r'send_smscode/(?P<phone>1[3,5,7,8,9]\d{9})/', SendSmsCode.as_view()),
    re_path(r'check_smscode/(?P<phone>1[3,5,7,8,9]\d{9})/', CheckSmsCode.as_view()),
    # 邮箱验证码相关接口
    re_path(r'send_emailcode/(?P<email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/', SendEmailCode.as_view()),
    re_path(r'check_emailcode/(?P<email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/', CheckEmailCode.as_view()),

]
import random
import re
import string

import django_redis
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from QTribe.utils.smscode import send_sms_code
from verify_code.models import EmailVerifyCode


# 固定邮箱验证码，方便测试
FIXED_EMAIL_CODE = '123456'


class SendSmsCode(View):
    def get(self,request,phone):
        #生成验证码
        num=string.digits
        num_list=random.choices(num,k=6)
        code=''.join(num_list)
        #将code保存到redis数据库中
        redis_conn=django_redis.get_redis_connection('verify_code')
        redis_conn.setex(f'sms{phone}',60,code)
        # ret=send_sms_code(code, phone)
        ret={'code':2}
        if ret.get('code')==2:
            return JsonResponse({'code':'200','errormsg':'ok'})
        return JsonResponse({'code':'5001','errormsg':'短信发送错误'})

class CheckSmsCode(View):
    def get(self,request,phone):
        #接收参数
        code=request.GET.get('smscode')
        if not all([phone,code]):
            return JsonResponse({'code':'4001'})
        #将该电话号码对应的验证码从数据库中提取出来
        redis_conn=django_redis.get_redis_connection('verify_code')
        code_real=redis_conn.get(f'sms{phone}')
        if code_real is None:
            return JsonResponse({'code':'4002','errormsg':'验证码已过期'})
        if code_real.decode('utf-8')!=code:
            return JsonResponse({'code':'4003','errormsg':'验证码错误'})
        return JsonResponse({'code':200,'errormsg':'ok'})


class SendEmailCode(View):
    """发送邮箱验证码"""
    def get(self, request, email):
        # 校验邮箱格式
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return JsonResponse({'code': '4001', 'errormsg': '邮箱格式不正确'})

        # 使用固定验证码方便测试
        code = FIXED_EMAIL_CODE

        # 将验证码保存到Redis中，有效期10分钟
        redis_conn = django_redis.get_redis_connection('verify_code')
        redis_conn.setex(f'email_{email}', 600, code)

        # 同时保存到数据库中做记录
        EmailVerifyCode.objects.create(email=email, code=code, type='1')

        # TODO: 后续接入SMTP发送邮件服务
        # 目前返回验证码方便前端测试（生产环境应移除）
        return JsonResponse({
            'code': '200',
            'errormsg': 'ok',
            'data': {
                'email': email,
                'code': code  # 测试阶段返回验证码，方便验证
            }
        })


class CheckEmailCode(View):
    """校验邮箱验证码"""
    def get(self, request, email):
        code = request.GET.get('emailcode')

        if not all([email, code]):
            return JsonResponse({'code': '4001', 'errormsg': '缺少必传参数'})

        # 从Redis中获取验证码
        redis_conn = django_redis.get_redis_connection('verify_code')
        code_real = redis_conn.get(f'email_{email}')

        if code_real is None:
            return JsonResponse({'code': '4002', 'errormsg': '验证码已过期'})

        if code_real.decode('utf-8') != code:
            return JsonResponse({'code': '4003', 'errormsg': '验证码错误'})

        return JsonResponse({'code': '200', 'errormsg': 'ok'})


class SendEmailCodeForReset(View):
    """发送邮箱验证码（用于找回密码）"""
    def get(self, request, email):
        # 校验邮箱格式
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return JsonResponse({'code': '4001', 'errormsg': '邮箱格式不正确'})

        # 使用固定验证码方便测试
        code = FIXED_EMAIL_CODE

        # 将验证码保存到Redis中，有效期10分钟
        redis_conn = django_redis.get_redis_connection('verify_code')
        redis_conn.setex(f'email_reset_{email}', 600, code)

        # 同时保存到数据库中做记录
        EmailVerifyCode.objects.create(email=email, code=code, type='2')

        return JsonResponse({
            'code': '200',
            'errormsg': 'ok',
            'data': {
                'email': email,
                'code': code  # 测试阶段返回验证码，方便验证
            }
        })

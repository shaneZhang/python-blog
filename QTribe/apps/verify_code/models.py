from django.db import models

# Create your models here.
from QTribe.utils.base_model import BaseModel2


class EmailVerifyCode(BaseModel2):
    """邮箱验证码模型"""
    email = models.EmailField(verbose_name='邮箱地址', max_length=254)
    code = models.CharField(verbose_name='验证码', max_length=6)
    # 验证码类型：1-注册 2-找回密码 3-修改邮箱
    type = models.CharField(verbose_name='验证码类型', max_length=1, default='1')

    class Meta:
        db_table = 't_email_verify_code'
        verbose_name = '邮箱验证码表'
        verbose_name_plural = verbose_name

from django.db import models

class User(models.Model):
    idx = models.AutoField(verbose_name='index', primary_key=True)
    user_id = models.CharField(max_length=32, unique=True, verbose_name='유저 아이디')
    user_pwd = models.CharField(max_length=128, verbose_name='유저 비밀번호')
    user_name = models.CharField(max_length=16, unique=True, verbose_name='유저 이름')
    user_email = models.EmailField(max_length=128, verbose_name='유저 이메일')
    user_register_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='등록일')
    user_auth = models.SmallIntegerField(default=0, null=True, verbose_name='유저 권한')
    
    class Meta:
        db_table = 'user'
        verbose_name = '유저'
        verbose_name_plural = '유저'
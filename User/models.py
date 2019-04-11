from django.contrib.auth.hashers import make_password, check_password
from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32, unique=True, verbose_name='用户名')
    nick_name = models.CharField(max_length=32, unique=True, verbose_name='昵称')
    _password = models.CharField(max_length=256, verbose_name='密码')
    avatar_url = models.CharField(max_length=256, null=True, verbose_name='头像')
    is_delete = models.BooleanField(default=0, verbose_name='是否删除')

    class Meta:
        db_table = 'news_User'

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        self._password = make_password(pwd, None, 'pbkdf2_sha256')
        return self._password

    def check_password(self, pwd):
        print(pwd)
        return check_password(pwd, self._password,None, 'pbkdf2_sha256')


class User_Fans(models.Model):
    follower_id = models.IntegerField()
    followed_id = models.IntegerField()

    class Meta:
        db_table = 'news_User_Fans'

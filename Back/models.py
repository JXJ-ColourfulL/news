from django.contrib.auth.hashers import make_password, check_password
from django.db import models

# Create your models here.
class Auther(models.Model):
    authername = models.CharField(max_length=32, unique=True, verbose_name='用户名')
    nickname = models.CharField(max_length=32, unique=True, verbose_name='昵称')
    _password = models.CharField(max_length=256, verbose_name='密码')
    avatar_url = models.CharField(max_length=256, null=True, verbose_name='头像')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    permission = models.IntegerField(default=1,verbose_name='权限')
    is_delete = models.BooleanField(default=0, verbose_name='是否删除')

    class Meta:
        db_table = 'news_Auther'

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
    def to_simple_dict(self):
        simple_dict={
            'auther_id':self.id,
            'nickname':self.nickname,
            'create_time':self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'avatar_url':self.avatar_url,
        }
        return simple_dict
    def to_dict(self):
        auther_dict = {
            'auther_id':self.id,
            'nickname':self.nickname,
            'authername':self.authername,
            'avatar_url':self.avatar_url,
            'create_time':self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return auther_dict
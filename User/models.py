from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32,unique=True,verbose_name='用户名')
    nick_name = models.CharField(max_length=32,unique=True,verbose_name='昵称')
    password = models.CharField(max_length=256,verbose_name='密码')
    avatar_url = models.CharField(max_length=256,null=True,verbose_name='头像')
    is_delete = models.BooleanField(default=0,verbose_name='是否删除')
    class Meta:
        db_table='news_User'


class User_Fans(models.Model):
    follower_id = models.IntegerField()
    followed_id = models.IntegerField()
    class Meta:
        db_table='news_User_Fans'

from django.db import models

# Create your models here.
from User.models import User


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='新闻分类')
    class Meta:
        db_table='news_Category'

class News(models.Model):
    title = models.CharField(max_length=64,unique=True,verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    create_time = models.DateTimeField(verbose_name='发布时间')
    index_img_url = models.CharField(max_length=256,null=True,verbose_name='新闻图片')
    clicks = models.IntegerField(default=0,verbose_name='点击量')
    comments_count = models.IntegerField(default=0,verbose_name='评论数')
    digest = models.CharField(max_length=128,verbose_name='描述')
    publish = models.ForeignKey(User)
    category = models.ForeignKey(Category)

    class Meta:
        db_table='news_News'

class User_Collection(models.Model):
    user_id = models.ForeignKey(User)
    news_id = models.ForeignKey(News)
    class Meta:
        db_table='news_User_Collection'




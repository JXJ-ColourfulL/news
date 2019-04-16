import uuid

from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from News.models import News
from User.models import User
from common import keys, state
from libs.nqcloud import upload_qncloud


def save_publish(publish):
    user = User.objects.filter(username=publish).first()
    if not user:
        user = User()
        user.username = publish
        user.password = '111111'
        user.nick_name = publish
        user.save()
    return user.id


def save_image(index_image, filename):
    image_data = index_image.read()
    _, url = upload_qncloud(filename, image_data)
    return url


def get_paging(page,uniq):

    if page == 1:
        uniq = str(uuid.uuid4())
        key = keys.NEW_LIST_KEY % uniq
        news_list = News.objects.all().order_by('-create_time')
        cache.set(key, news_list)
    else:
        key = keys.NEW_LIST_KEY % uniq
        news_list = cache.get(key)
    # 创建paginator对象 需两个参数 参数1为要被分页的对象，参数2为每页显示数量
    paginator = Paginator(news_list, state.PER_PAGE)
    try:
        # 获取pages对象传递给页面
        pages = paginator.page(page)
    # 	当传递页数的参数不为整数时，页码默认为1（一般在刷新页面时）
    except PageNotAnInteger:
        pages = paginator.page(1)
    # 	当页面为空时，将显示最后一页内容
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return pages, uniq

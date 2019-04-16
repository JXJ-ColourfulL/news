from django.core.cache import cache
from django.http import HttpResponse

from News.logics import get_paging
from News.models import News

from common import keys, state
from libs.http import render_json





def get_swiper(request):
    """
    首页轮播图
    :param request:
    :return:
    """
    news_list = cache.get(keys.SWIPER_CACHE_KEY)
    if news_list:
        print('cache')
        return render_json(data=news_list)
    news = News.objects.order_by('create_time')[:4]
    news_list = []
    for new in news:
        new_dict = {
            'new_url': new.index_img_url,
            'new_id': new.id,
        }
        news_list.append(new_dict)
        cache.set(keys.SWIPER_CACHE_KEY, news_list, state.SWIPER_CACHE_TIMEOUT)
    return render_json(data=news_list)


def push_news(request):
    """
    首页推荐新闻
    :param request:
    :return:
    """
    news_list = cache.get(keys.HOME_REMD_KEY)
    if news_list:
        print('cache')
        return render_json(news_list)

    news = News.objects.order_by('create_time')[4:9]
    news_list = [new.to_less_dict() for new in news]
    cache.set(keys.HOME_REMD_KEY, news_list, state.NEWS_CACHE_TIMEOUT)
    return render_json(news_list)


def new_lists(request):
    """
    获取所有新闻列表
    :param request:
    :return:
    """

    # last_id = request.GET.get('new_last_id')
    page = int(request.GET.get('page', 1))
    uniq = request.GET.get('uniq')
    pages,nuniq = get_paging(page,uniq)
    news_lists = [new.to_less_dict() for new in pages]
    return render_json(data=news_lists,uniq=nuniq)


def new_detail(request):
    """
    新闻页面详情
    :param request:
    :return:
    """
    new_id = request.GET.get('new_id')
    cache_key = keys.NEW_DETAIL_KEY % new_id
    data = cache.get(cache_key)
    if data:
        return render_json(data=data)
    new = News.objects.get(id=new_id)
    data = new.to_dict()
    cache.set(cache_key, data, state.NEWS_DETAIL_CACHE_TIMEOUT)
    return render_json(data=data)

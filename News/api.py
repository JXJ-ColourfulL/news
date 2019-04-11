from django.http import HttpResponse

from News.logics import save_news
from News.models import News
from User.logics import get_paging
from libs.http import render_json


def get_news(request):
    """
    保存新闻
    :param request:
    :return:
    """
    title = request.POST.get('title')
    content = request.POST.get('content')
    create_time = request.POST.get('create_time')
    index_img_url = request.POST.get('index_img_url')
    publish = request.POST.get('publish')
    category_id = request.POST.get('category_id')
    digest = request.POST.get('digest')
    save_news(publish, title, content, create_time, index_img_url, category_id, digest)
    return HttpResponse('ok')


def get_swiper(request):
    """
    首页轮播图
    :param request:
    :return:
    """
    news = News.objects.order_by('create_time')[:4]
    news_list = []
    for new in news:
        new_dict = {
            'new_url': new.index_img_url,
            'new_id': new.id,
        }
        news_list.append(new_dict)
    return render_json(data=news_list)


def push_news(request):
    """
    首页推荐新闻
    :param request:
    :return:
    """
    news = News.objects.order_by('create_time')[4:9]
    news_list = [new.to_less_dict() for new in news]
    return render_json(news_list)


def new_lists(request):
    """
    获取所有新闻列表
    :param request:
    :return:
    """
    last_id = request.GET.get('new_id',10)
    page = int(request.GET.get('page',1))
    pages = get_paging(page,last_id)
    news_lists = [new.to_less_dict() for new in pages]
    return render_json(data=news_lists)


def new_detail(request):
    """
    新闻页面详情
    :param request:
    :return:
    """
    new_id = request.GET.get('new_id')

    new = News.objects.get(id=new_id)
    data = new.to_dict()
    return render_json(data=data)
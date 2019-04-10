from django.http import HttpResponse

from News.logics import save_news


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
    save_news(publish,title,content,create_time,index_img_url,category_id,digest)
    return HttpResponse('ok')
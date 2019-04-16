import uuid

from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from News.logics import save_publish
from News.models import News
from common import status_code, keys
from libs.http import render_json
from libs.nqcloud import upload_qncloud


def save_news(publish,title,content,create_time,index_img_url,category_id,digest):
    user_id = save_publish(publish)
    # filename = 'new_image_%s' % create_time
    # index_img_url=save_image(index_img,filename)
    new = News.objects.filter(title=title).first()
    if not new:
        new = News()
        new.title=title
        new.content = content
        new.create_time = create_time
        new.index_img_url = index_img_url
        new.publish_id = user_id
        new.category_id = category_id
        new.digest = digest
        new.save()
        return True
    return False


def check_auther_params(authername, password, nickname):
    """
    验证参数
    :param authername: 用户名
    :param password: 密码
    :param nickname: 昵称
    :return:
    """
    if not all([authername, password, nickname]):
        return render_json(code=status_code.PARMERR,resultValue='参数缺失')
    auther = News.objects.filter(authername=authername).first()
    if auther:
        return render_json(code=status_code.PARMERR,resultValue='此用户名已被使用')
    auther = News.objects.filter(nickname=nickname).first()
    if auther:
        return render_json(code=status_code.PARMERR,resultValue='昵称已被使用')
    return True


def save_avatar(filename, data):
    """
    保存头像
    :param data: 头像图片
    :param username: 用户名auth_user
    :return: url: 头像路径
    """
    avatar_data = data.read()
    status,url = upload_qncloud(filename,avatar_data)
    print(url)
    if not status:
        return render_json(code=status_code.THIRDERR,resultValue='头像保存失败')
    return url


def get_pags(page,per_page,keyword):
    auther = News.objects.filter(nickname__contains=keyword).filter(is_delete=0).order_by('-create_time')
    paginator = Paginator(auther, per_page)
    try:
        # 获取pages对象传递给页面
        pages = paginator.page(page)
    # 	当传递页数的参数不为整数时，页码默认为1（一般在刷新页面时）
    except PageNotAnInteger:
        pages = paginator.page(1)
    # 	当页面为空时，将显示最后一页内容
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return pages


def delete_cache():
    cache.delete(keys.AUTHER_DES_KEY)
    cache.delete(keys.AUTHER_ASC_KEY)


def delete_news_cache():
    cache.delete(keys.NEWS_DES_KEY)
    cache.delete(keys.NEWS_ASC_KEY)


def new_pages(page,per_page,auther_id):
    news = News.objects.filter(is_delete=0, publish_id=auther_id).order_by('-create_time')
    print(news)
    paginator = Paginator(news, per_page)
    try:
        # 获取pages对象传递给页面
        pages = paginator.page(page)
    # 	当传递页数的参数不为整数时，页码默认为1（一般在刷新页面时）
    except PageNotAnInteger:
        pages = paginator.page(1)
    # 	当页面为空时，将显示最后一页内容
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return pages



def search_new_pages(page,per_page,search_keyword,auther_id):
    news = News.objects.filter(is_delete=0,publish_id=auther_id,title__contains=search_keyword).order_by('-create_time')
    paginator = Paginator(news, per_page)
    try:
        # 获取pages对象传递给页面
        pages = paginator.page(page)
    # 	当传递页数的参数不为整数时，页码默认为1（一般在刷新页面时）
    except PageNotAnInteger:
        pages = paginator.page(1)
    # 	当页面为空时，将显示最后一页内容
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return pages




def sort_page(types,sort_type,page,per_page):
    if types == 'auther':
        if sort_type == 'des':
            datas = News.objects.filter(is_delete=0).order_by('-create_time')
        elif sort_type == 'asc':
            datas = News.objects.filter(is_delete=0).order_by('create_time')
        else:
            return False

    elif types == 'new':
        if sort_type == 'des':
            datas = News.objects.filter(is_delete=0).order_by('-create_time')
        elif sort_type == 'asc':
            datas = News.objects.filter(is_delete=0).order_by('create_time')
        else:
            return False

    paginator = Paginator(datas, per_page)
    try:
        # 获取pages对象传递给页面
        pages = paginator.page(page)
    # 	当传递页数的参数不为整数时，页码默认为1（一般在刷新页面时）
    except PageNotAnInteger:
        pages = paginator.page(1)
    # 	当页面为空时，将显示最后一页内容
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return pages






def check_new_params(new_title,new_digest,new_content,auther_id,new_image):
    if not all([new_title,new_digest,new_content,auther_id]):
        return render_json(code=status_code.PARMERR,resultValue='参数缺失')
    new = News.objects.filter(title=new_title).first()
    if not new:
        if new_image !=None:
            ranuid = uuid.uuid4()
            filename = 'New_%s_%s'%(auther_id,ranuid)
            index_img_url = save_avatar(filename,new_image)
        else:
            index_img_url = 'null'
        new = News()
        new.title=new_title
        new.content = new_content
        new.index_img_url = index_img_url
        new.publish_id = auther_id
        new.category_id = 1
        new.digest = new_digest
        new.save()
        return True
    return False
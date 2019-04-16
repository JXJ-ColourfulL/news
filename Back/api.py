import uuid

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Back import logics
from Back.logics import save_news, get_pags, new_pages, check_new_params, search_new_pages, sort_page
from Back.models import Auther
from News.models import News
from User.logics import save_avatar
from common import status_code, state, keys
from libs.http import render_json
from libs.permission import check_permission


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


def login(request):
    """
    登入
    :param request:
    :return:
    """
    authername = request.POST.get('authername')
    password = request.POST.get('password')

    auther = Auther.objects.filter(authername=authername).first()
    if not auther:
        return render_json(code=status_code.LOGINERR, resultValue='用户名错误')
    if not auther.check_password(password):
        return render_json(code=status_code.LOGINERR, resultValue='用户名或密码错误')

    request.session['auid'] = auther.id
    return render_json()


@check_permission(state.PERMIS)
def auther(request):
    """
    后台用户页面
    :param request:
    :return:
    """
    # key = keys.AUTHER_DES_KEY
    # authers_list = cache.get(key)
    # if authers_list:
    #     return render_json(data=authers_list)
    authers = News.objects.filter(is_delete=0).order_by('-create_time')
    authers_list = [auther.to_simple_dict() for auther in authers]
    # cache.set(key, authers_list)
    return render_json(data=authers_list)


@check_permission(state.PERMIS)
def auther_sort(request):
    """
    作者排序
    :param request:
    :return:
    """
    sort_type = request.GET.get('sort_type')
    try:
        page = int(request.GET.get('page', 1))
    except ValueError as e:
        page = 1
    try:
        per_page = int(request.GET.get('per_page', 10))
    except ValueError:
        per_page = 10
    if not sort_type:
        return render_json(code=status_code.PARMERR, resultValue='参数缺失')
    authers = sort_page('auther', sort_type, page, per_page)
    if authers == False:
        return render_json(code=status_code.PARMERR, resultValue='参数错误')
    authers_list = [auther.to_simple_dict() for auther in authers]
    return render_json(data=authers_list)


@check_permission(state.PERMIS)
def append_auther(request):
    """
    添加作者
    :param request:
    :return:
    """
    authername = request.POST.get('authername')
    password = request.POST.get('password')
    nickname = request.POST.get('nickname')
    avatar = request.FILES.get('avatar')
    logics.check_auther_params(authername, password, nickname)

    if avatar == None:
        avatar_url = state.DEFAULT_AVATAR_URL
    else:
        uid = uuid.uuid4()
        filename = "New_avatar_%s" % uid
        avatar_url = logics.save_avatar(filename, avatar)

    auther = News(authername=authername, nickname=nickname, avatar_url=avatar_url)
    auther.password = password
    try:
        auther.save()
    except Exception:
        return render_json(code=status_code.PARMERR, resultValue='此用户名已被注册')

    return render_json()


@check_permission(state.PERMIS)
def confirm_auther(request):
    """
    作者保存修改
    :param request:
    :return:
    """
    authername = request.POST.get('authername')
    password = request.POST.get('password')
    nickname = request.POST.get('nickname')
    avatar = request.FILES.get('avatar')
    auther_id = request.POST.get('auther_id')
    if not all([authername, password, nickname, auther_id]):
        return render_json(code=status_code.PARMERR, resultValue='参数缺失')
    if avatar == None:
        return render_json(code=status_code.PARMERR, resultValue='请上传头像')
    nauther = News.objects.filter(nickname=nickname).first()
    if nauther:
        if nauther.id != auther_id:
            return render_json(code=status_code.PARMERR, resultValue='昵称已被使用')
    uid = uuid.uuid4()
    filename = "New_avatar_%s" % uid
    avatar_url = logics.save_avatar(filename, avatar)
    auther = News.objects.get(id=auther_id)
    auther.nickname = nickname
    auther.password = password
    auther.avatar_url = avatar_url
    try:
        auther.save()
    except Exception as e:
        print(e)
    # logics.delete_cache()
    return render_json()


@check_permission(state.PERMIS)
def modify_auther(request):
    """
    修改
    :param request:
    :return:
    """
    auther_id = request.GET.get('auther_id')
    auther = News.objects.get(id=auther_id)
    if auther.is_delete == 1:
        return render_json(code=status_code.NODATA, resultValue='用户不存在')
    # logics.delete_cache()
    return render_json(data=auther.to_dict())


@check_permission(state.PERMIS)
def search_auther(request):
    """
    搜索作者
    :param request:
    :return:
    """
    keyword = request.GET.get('search_keyword')
    try:
        page = int(request.GET.get('page', 1))
    except ValueError as e:
        page = 1
    try:
        per_page = int(request.GET.get('per_page', 10))
    except ValueError:
        per_page = 10
    page = get_pags(page, per_page, keyword)
    auther_lists = [auther.to_simple_dict() for auther in page]

    return render_json(data=auther_lists)


@check_permission(state.PERMIS)
def remove_auther(request):
    """
    删除作者
    :param request:
    :return:
    """
    auther_id = request.GET.get('auther_id')
    auther = News.objects.get(id=auther_id)
    auther.is_delete = 1
    auther.save()
    logics.delete_cache()
    return render_json()


def news(request):
    """
    进入新闻页面
    :param request:
    :return:
    """
    re_auther = request.auther
    auther_id = request.GET.get('auther_id')
    try:
        page = int(request.GET.get('page', 1))
    except ValueError as e:
        page = 1
    try:
        per_page = int(request.GET.get('per_page', 10))
    except ValueError:
        per_page = 10
    auther = Auther.objects.get(id=auther_id)
    if re_auther != auther:
        return render_json(code=status_code.EXEERR, resultValue='登入用户与操作用户不一致')

    news = new_pages(page, per_page, auther_id)
    print(news)
    news_list = [new.to_less_dict() for new in news]
    return render_json(data=news_list)


def append_new(request):
    """
    添加新闻
    :param request:
    :return:
    """
    new_title = request.POST.get('new_title')
    new_digest = request.POST.get('new_digest')
    new_content = request.POST.get('new_content')
    auther_id = request.POST.get('auther_id')
    new_image = request.FILES.get('new_image')
    if not check_new_params(new_title, new_digest, new_content, auther_id, new_image):
        return render_json(code=status_code.DATAEXITERR, resultValue='新闻已存在')
    # logics.delete_news_cache()
    return render_json()


def modify_new(request):
    """
    修改新闻
    :param request:
    :return:
    """
    new_id = request.GET.get('new_id')
    auther_id = request.GET.get('auther_id')
    new = News.objects.filter(id=new_id, publish_id=auther_id).first()
    return render_json(data=new.to_dict())


def confirm_new(request):
    """
    确认修改
    :param request:
    :return:
    """
    new_title = request.POST.get('new_title')
    new_digest = request.POST.get('new_digest')
    new_content = request.POST.get('new_content')
    auther_id = request.POST.get('auther_id')
    new_id = int(request.POST.get('new_id'))
    new_image = request.FILES.get('new_image')

    if not all([new_title, new_digest, new_content, auther_id, new_id]):
        return render_json(code=status_code.PARMERR, resultValue='参数缺失')
    new = News.objects.filter(title=new_title).first()
    if new:
        if new.id != new_id:
            return render_json(code=status_code.PARMERR, resultValue='文章标题已被使用')
    if new_image != None:
        ranuid = uuid.uuid4()
        filename = 'New_%s_%s' % (auther_id, ranuid)
        index_img_url = save_avatar(filename, new_image)
    else:
        index_img_url = 'null'

    new = News.objects.get(id=new_id)
    new.title = new_title
    new.content = new_content
    new.index_img_url = index_img_url
    new.digest = new_digest
    new.save()
    # logics.delete_news_cache()
    return render_json()


def search_new(request):
    """
    搜索新闻
    :param request:
    :return:
    """
    auther_id = request.auther.id

    keyword = request.GET.get('search_keyword')
    try:
        page = int(request.GET.get('page', 1))
    except ValueError as e:
        page = 1
    try:
        per_page = int(request.GET.get('per_page', 10))
    except ValueError:
        per_page = 10

    page = search_new_pages(page, per_page, keyword, auther_id)
    new_lists = [new.to_less_dict() for new in page]
    return render_json(data=new_lists)


def news_sort(request):
    """
    新闻排序
    :param request:
    :return:
    """
    sort_type = request.GET.get('sort_type')
    try:
        page = int(request.GET.get('page', 1))
    except ValueError as e:
        page = 1
    try:
        per_page = int(request.GET.get('per_page', 10))
    except ValueError:
        per_page = 10
    if not sort_type:
        return render_json(code=status_code.PARMERR, resultValue='参数缺失')
    news = sort_page('new', sort_type, page, per_page)
    if news == False:
        return render_json(code=status_code.PARMERR, resultValue='参数错误')
    new_lists = [new.to_less_dict() for new in news]
    return render_json(data=new_lists)


def remove_new(request):
    """
    删除新闻
    :param request:
    :return:
    """
    new_id = request.GET.get('new_id')
    new = News.objects.get(id=new_id)
    new.is_delete = 1
    new.save()
    # logics.delete_news_cache()
    return render_json()


def logout(request):
    """
    登出
    :param request:
    :return:
    """
    request.session.flush()
    return render_json()

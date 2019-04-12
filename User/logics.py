from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from News.models import News
from User.models import User
from libs.http import render_json
from common import status_code, state, keys
from libs.nqcloud import upload_qncloud


def check_params(username,password,repassword,nickname):
    """
    验证参数
    :param username: 用户名
    :param password: 密码
    :param repassword: 确认密码
    :param nickname: 昵称
    :return:
    """
    if not all([username,password,repassword,nickname]):
        return render_json(code=status_code.PARMERR,resultValue='参数缺失')
    if password !=repassword:
        return render_json(code=status_code.PARMERR,resultValue='两次密码不一致')

    user = User.objects.filter(username=username).first()
    if user:
        return render_json(code=status_code.PARMERR,resultValue='此用户名已被注册')
    user = User.objects.filter(nick_name=nickname).first()
    if user:
        return render_json(code=status_code.PARMERR,resultValue='昵称已被使用')
    return True

def save_avatar(avatar,username):
    """
    保存头像
    :param avatar: 头像图片
    :param username: 用户名auth_user
    :return: url: 头像路径
    """
    filename = "New_avatar_%s" % username
    avatar_data = avatar.read()
    status,url = upload_qncloud(filename,avatar_data)
    print(url)
    if not status:
        return render_json(code=status_code.THIRDERR,resultValue='头像保存失败')
    return url


def get_paging(page,new_id):
    # 查询数据库中所有数据
    news_list = News.objects.all().order_by('-create_time')
    if page != 1:
        news_list = news_list.filter(id__lt=new_id)
    # 创建paginator对象 需两个参数 参数1为要被分页的对象，参数2为每页显示数量
    paginator = Paginator(news_list, state.PER_PAGE)
    try:
        # 获取pages对象传递给页面
        pages = paginator.page(1)
    # 	当传递页数的参数不为整数时，页码默认为1（一般在刷新页面时）
    except PageNotAnInteger:
        pages = paginator.page(1)
    # 	当页面为空时，将显示最后一页内容
    except EmptyPage:
        old_new_id = int(new_id)-int(new_id)%int(state.PER_PAGE)
        old_page = int(page)-1
        key = keys.NEW_LIST_KEY %(old_page,old_new_id)
        pages = cache.get(key)
        return render_json(data=pages)
    return pages
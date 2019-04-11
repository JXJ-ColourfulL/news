from django.http import QueryDict

from User import logics
from User.models import User
from common import status_code
from common import state
from libs.http import render_json


def get_user(request):
    """
    获取个人信息
    :param request:
    :return:
    """
    uid = request.session.get('uid')
    if uid:
        user = User.objects.get(id=uid)
        data = {
            'nickname': user.nick_name,
            'user_id': user.id,
            'avatar_url': user.avatar_url,
        }
        return render_json(data=data)
    return render_json()


def register(request):
    """
    注册
    :param request:
    :return:
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    repassword = request.POST.get('repaswword')
    nickname = request.POST.get('nickname')
    avatar = request.FILES.get('avatar')
    logics.check_params(username, password, repassword, nickname)

    if avatar == None:
        avatar_url = state.DEFAULT_AVATAR_URL
    else:
        avatar_url = logics.save_avatar(avatar, username)

    user = User(username=username, nick_name=nickname, avatar_url=avatar_url)
    user.password = password
    try:
        user.save()
    except Exception:
        return render_json(code=status_code.PARMERR, resultValue='此用户名已被注册')
    return render_json()


def login(request):
    """
    登入
    :param request:
    :return:
    """
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = User.objects.filter(username=username).first()
    if not user:
        return render_json(code=status_code.LOGINERR, resultValue='用户名错误')
    if not user.check_password(password):
        return render_json(code=status_code.LOGINERR, resultValue='用户名或密码错误')

    request.session['uid'] = user.id
    return render_json()


def logout(request):
    """
    登出
    :param request:
    :return:
    """
    request.session.flush()
    return render_json()


def update_avatar(request):
    """
    修改头像
    :param request:
    :return:
    """
    user = request.user
    avatar = request.FILES.get('avatar')

    avatar_url = logics.save_avatar(avatar, user.username)
    user.avatar_url = avatar_url
    user.save()
    data = {
        'user_id': user.id,
        'avatar_url': avatar_url,
    }
    return render_json(data=data)

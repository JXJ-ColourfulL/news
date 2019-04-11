from User import logics
from User.models import User
from common import status_code
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
        data={
            'nickname':user.nick_name,
            'user_id':user.id,
            'avatar':user.avatar_url,
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

    avatar_url = logics.save_avatar(avatar, username)

    user = User(username=username, nick_name=nickname, avatar_url=avatar_url)
    user.password = password
    user.save()
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

from User import logics
from User.models import User
from libs.http import render_json


def get_user_info(request):
    return None


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
    return None


def logout(request):
    return None

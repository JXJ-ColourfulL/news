from django.utils.deprecation import MiddlewareMixin

from Back.models import Auther
from User.models import User
from common import status_code
from libs.http import render_json


class UserMiddleware(MiddlewareMixin):
    WHITE_LIST = [
        '/api/user/get_user/',
        '/api/user/logout/',
        '/api/user/update_avatar/',
    ]
    WHITE_AUTHER_LIST =[
        '/api/back/auther/',
        '/api/back/auther_sort/',
        '/api/back/append_auther/',
        '/api/back/confirm_auther/',
        '/api/back/modify_auther/',
        '/api/back/search_auther/',
        '/api/back/remove_auther/',
        '/api/back/news/',
        '/api/back/append_new/',
        '/api/back/modify_new/',
        '/api/back/confirm_new/',
        '/api/back/search_new/',
        '/api/back/news_sort/',
        '/api/back/remove_new/',
    ]

    def process_request(self, request):
        if request.path in self.WHITE_LIST:
            print('aaa')
            uid = request.session.get('uid')
            if uid:
                request.user = User.objects.get(id=uid)
                return
            return render_json(code=status_code.SESSIONERR, resultValue='用户未登入')
        elif request.path in self.WHITE_AUTHER_LIST:
            print('bbbb')
            auid = request.session.get('auid')
            print(auid)
            if auid:
                request.auther = Auther.objects.get(id=auid)
                return
            return render_json(code=status_code.SESSIONERR, resultValue='用户未登入')
        else:
            return
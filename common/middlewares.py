from django.utils.deprecation import MiddlewareMixin

from User.models import User
from common import status_code
from libs.http import render_json


class UserMiddleware(MiddlewareMixin):
    WHITE_LIST = [
        '/api/user/register/',
        '/api/user/login/',
        '/api/news/get_news/',
    ]

    def process_request(self, request):
        if request.path in self.WHITE_LIST:
            return

        uid = request.session.get('uid')
        if uid:
            request.user = User.objects.get(id=uid)
            return
        return render_json(code=status_code.SESSIONERR, resultValue='用户未登入')

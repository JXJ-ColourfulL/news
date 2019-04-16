from common import status_code
from libs.http import render_json


def check_permission(permission):
    def check_permission_fun(func):
        def check(request):
            auther = request.auther
            print(auther)
            if auther.permission !=permission:
                return render_json(status_code.PERMISSIONERR,resultValue='无权访问')
            else:
                return func(request)
        return check
    return check_permission_fun
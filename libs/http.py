import json

from django.http import HttpResponse

from common import status_code


def render_json(data=None, code=status_code.OK, resultValue='OK', **uniq):
    result = {
        'code': code,
        'data': data,
        'resultValue': resultValue,
    }
    result.update(uniq)
    print(result)
    json_result = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    return HttpResponse(json_result)

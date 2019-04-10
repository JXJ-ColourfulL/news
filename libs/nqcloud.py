from urllib.parse import urljoin

from qiniu import Auth, put_data
from news import config

def upload_qncloud(filename, filepath):
    # 创建对象
    q = Auth(config.QN_ACCESSKEY, config.QN_SECRETKEY)

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(config.QN_BUCKET, filename, 3600)
    # 上传至七牛云
    ret, info = put_data(token, filename, filepath)
    if info.ok():
        url = urljoin(config.QN_URL, filename)
        return True, url
    return False, " "
from News.models import News
from User.models import User
from libs.nqcloud import upload_qncloud


def save_publish(publish):

    user= User.objects.filter(username=publish).first()
    if not user:
        user = User()
        user.username = publish
        user.password = '111111'
        user.nick_name = publish
        user.save()
    return user.id

def save_image(index_image,filename):
    image_data = index_image.read()
    _,url = upload_qncloud(filename,image_data)
    return url

def save_news(publish,title,content,create_time,index_img_url,category_id,digest):
    user_id = save_publish(publish)
    # filename = 'new_image_%s' % create_time
    # index_img_url=save_image(index_img,filename)
    new = News.objects.filter(title=title).first()
    print(new)
    if not new:
        new = News()
        new.title=title
        new.content = content
        new.create_time = create_time
        new.index_img_url = index_img_url
        new.publish_id = user_id
        new.category_id = category_id
        new.digest = digest
        new.save()
        return True
    return False


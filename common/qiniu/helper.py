from django.conf import settings
from qiniu import Auth, PersistentFop, build_op, op_save, urlsafe_base64_encode


q = Auth(settings.QINIU_AK, settings.QINIU_SK)

key = 'my-python-logo.png'
bucket_name = 'Bucket_Name'
token = q.upload_token(bucket_name, key, 3600)
localfile = './sync/bbb.jpg'


def upload_file(token, key, localfile, version='v2'):
    ret, info = put_file(token, key, localfile, version)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)


def upload_video(bucket, key, pipeline, fops):
    saveas_key = urlsafe_base64_encode('目标Bucket_Name:自定义文件key')
    fops = fops + '|saveas/' + saveas_key
    pfop = PersistentFop(q, bucket, pipeline)
    ops = []
    ops.append(fops)
    ret, info = pfop.execute(key, ops, 1)
    return ret, info












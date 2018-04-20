# coding=utf-8

import qiniu

access_key = 'faZIkGvlnPqqHPLHeHcq6B537bLv4vmbh8xG0rlX'
secret_key = '7TUX_S0VBvnC9lskQpgSKuedMmNzUaYOUvS0YDsE'
bucket_name = 'ihomedjango'

q = qiniu.Auth(access_key, secret_key)

token = q.upload_token(bucket_name)

def push_img(data):
    ret, info = qiniu.put_data(token, None, data)
    if ret is not None:
        return ret
    else:
        return info # error message in info


if __name__ == '__main__':
    with open('home01.jpg') as f:
        print(push_img(f.read())['hash'])
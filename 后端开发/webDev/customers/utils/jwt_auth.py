
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import jwt
import datetime
from jwt import exceptions

JWT_SALT = 'iv%x6xo7l7_u9bf_u!9#g#m*)*=ej@bek5@u3kh*72+unjv='


def create_token(payload, timeout):
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + timeout
    result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers).decode('utf-8')
    return result

def parse_payload(token):
    """
    对token进行和发行校验并获取payload
    :param token:
    :return:
    """

    result = {'status': False, 'data': None, 'error': None}
    try:
        verified_payload = jwt.decode(token, JWT_SALT, True)
        result['status'] = True
        result['data'] = verified_payload
        #print(verified_payload)

    except exceptions.ExpiredSignatureError:
        result['error'] = 'token已失效'
    except jwt.DecodeError:
        result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['error'] = '非法的token'
    return result


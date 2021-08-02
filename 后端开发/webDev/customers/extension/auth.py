#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from customers.utils.jwt_auth import parse_payload
from customers.models import User

def authen(request):
    auth = JwtAuthorizationAuthentication()
    payload, token = auth.authenticate(request)
    user = User.objects.filter(username=payload['data']['username']).first()
    if user.is_active:
        return user
    else:
        return None


class JwtQueryParamAuthentication(BaseAuthentication):
    """
    用户需要在url中通过参数进行传输token，例如：
    http://www.pythonav.com?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzM1NTU1NzksInVzZXJuYW1lIjoid3VwZWlxaSIsInVzZXJfaWQiOjF9.xj-7qSts6Yg5Ui55-aUOHJS4KSaeLq5weXMui2IIEJU
    """

    def authenticate(self, request):
        token = request.content_params.get('token')
        payload = parse_payload(token)
        if not payload['status']:
            raise exceptions.AuthenticationFailed(payload)
        # 如果想要request.user等于用户对象，此处可以根据payload去数据库中获取用户对象。

        return (payload, token)


class JwtAuthorizationAuthentication(BaseAuthentication):
    """
    用户需要通过请求头的方式来进行传输token，例如：
    Authorization:jwt eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzM1NTU1NzksInVzZXJuYW1lIjoid3VwZWlxaSIsInVzZXJfaWQiOjF9.xj-7qSts6Yg5Ui55-aUOHJS4KSaeLq5weXMui2IIEJU
    """

    def authenticate(self, request):

        # 非登录页面需要校验token
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        auth = authorization.split()
        print(auth)
        if not auth:
            raise exceptions.AuthenticationFailed({'error': '未获取到Authorization请求头', 'status': False})
        if auth[1].lower() != 'jwt':
            raise exceptions.AuthenticationFailed({'error': 'Authorization请求头中认证方式错误', 'status': False})

        if len(auth) != 4:
            raise exceptions.AuthenticationFailed({'error': "非法Authorization请求头", 'status': False})
        version = auth[2]
        token = auth[3]
        result = parse_payload(token)
        if not result['status']:
            raise exceptions.AuthenticationFailed(result)
        user=User.objects.filter(username=result['data']['username']).first()
        if user.jwt_version!=version:
            raise exceptions.AuthenticationFailed({'error':"jwt版本错误"})
        # 如果想要request.user等于用户对象，此处可以根据payload去数据库中获取用户对象。
        return (result, token)


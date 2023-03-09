import json
import logging
import os
import requests
from urllib import parse

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from qzkj.models import User
from django.core.exceptions import ObjectDoesNotExist
from qzkj.settings import BASE_DIR

logger = logging.getLogger('log')


def verify(request):
    with open(os.path.join(BASE_DIR, 'MP_verify_yxSL8Vl2Cy7VfcHP.txt'), 'r') as f:
        str = f.readline()
    return HttpResponse(str)


def register(request, _):
    '''
    注册页面
    '''
    nickname = request.GET.get('nickname', None)
    openid = request.GET.get('openid', None)
    return render(request, 'register.html', context={'nickname':nickname, 'openid':openid})


def userinfo(request, _):
    '''
    用户信息显示
    '''
    nickname = request.GET.get('nickname', None)
    score = request.GET.get('score', 0)
    return render(request, 'user_info.html', context={'nickname':nickname, 'score': score})

def existed(opid):
    '''
    判断自己数据库中是否有用户信息
    '''
    try:
        res = User.objects.get(openid=opid)
        return True
    except ObjectDoesNotExist:
        return False


def get_user_info_from_wx(openid, access_token):
    url = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN'.format(access_token, openid)
    response = requests.get(url)
    response = json.loads(response.text)
    return response


def get_user_info_from_db(opid):
    user = User.objects.get(openid=opid)  
    logger.info(user.nick_name)   
    ctx = {'nickname': user.nick_name, 'uscore': user.score_nowithdraw+user.score_withdrawable}   
    return ctx


def get_user_info(request):
    '''
    用code换取access token，然后获取用户资料.
    参考https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html
    '''
    data = json.loads(request.body.decode('utf-8'))
    code = data['code']
    
    logger.info(code)
    if code == None:
        return HttpResponse('code and state not got in server.')
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx71b3d2f26d40ecbc&secret=39ceb0e5030cb2d2ce2d705f75945b67&code={}&grant_type=authorization_code'.format(code)
    response = requests.get(url)
    logger.info(response.text)
    response = json.loads(response.text)
    access_token = response['access_token']
    openid = response['openid']

    if existed(openid):
        # 用户注册过，信息在数据库中
        logger.info(openid)
        ctx = get_user_info_from_db(openid)   
        ctx['exist'] = 1
        return JsonResponse(ctx)
    else:
        # 从微信获取用户资料
        ctx = get_user_info_from_wx(openid, access_token)
        ctx['exist'] = 0
        return JsonResponse(ctx)


class RegisterView(View):
    sopenid = ''
    nickname = ''
    telephone = ''
    introducer = None
    score_nowithdraw = 30
    score_withdrawable = 0

    def post(self, request, _):
        '''
        注册
        '''
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            self.nickname = body['wx_nck']
            self.sopenid = body["opid"]
            self.telephone = body['pn']
            self.introducer = body['intro']
        except:
            return JsonResponse({'error': '哦吼，网络开小差了！'})  
            
        if self.introducer == '':
            self.introducer = None
        else:             
            res = User.objects.filter(telephone=self.introducer)
            if res.exists():
                self.introducer = res[0]
            else:
                return JsonResponse({'error': '介绍人不存在！'})

        
        user = User.objects.create(openid=self.sopenid, nick_name = self.nickname, telephone=self.telephone, introducer=self.introducer, score_nowithdraw=self.score_nowithdraw)
        user.save()
        return JsonResponse({'msg': '恭喜您注册成功！'})     


    

    
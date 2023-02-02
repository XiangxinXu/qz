import json
import logging
import os
import requests

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from qzkj.models import User
from django.core.exceptions import ObjectDoesNotExist
from qzkj.settings import BASE_DIR

logger = logging.getLogger('log')


def verify(request):
    with open(os.path.join(BASE_DIR, 'MP_verify_yxSL8Vl2Cy7VfcHP.txt'), 'r') as f:
        str = f.readline()
    return HttpResponse(str)

def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """
    return render(request, 'index.html')


def wxuser_auth(request, _):
    # url = "https://api.weixin.qq.com/cgi-bin/user/info?openid={}&lang=zh_CN".format(request.headers['x-wx-openid'])
    # response = requests.get(url)
    # logger.info(response.text)
    # logger.info('\nxxx\n')

    url = "https://api.weixin.qq.com/sns/userinfo?openid={}&lang=zh_CN".format(request.headers['x-wx-openid'])
    response = requests.get(url)
    logger.info(response.text)
    logger.info('\nxxx\n')
    return JsonResponse(response.json())


class UserView(View):
    wx_num = ''
    wx_nck = ''
    telephone = ''
    introducer = None
    score_nowithdraw = 0
    score_withdrawable = 0

    def post(self, request, _):
        '''
        注册
        '''
        # logger.info('req: {}'.format(request.body))
        
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            self.wx_num = body["wx_num"]
            self.wx_nck = body["wx_nck"]
            self.telephone = body['telephone']
            self.introducer = body['intro']
        except:
            return JsonResponse({'error': '哦吼，网络开小差了！'})

        if self.existed():
            return JsonResponse({'msg': '用户已存在！'})
        else:
            
            if self.introducer == '':
                self.introducer = None
            else:             
                res1 = User.objects.filter(telephone=self.introducer)
                res2 = User.objects.filter(user_name=self.introducer)
                if res1.exists():
                    self.introducer = res1[0]
                elif res2.exists():
                    self.introducer = res2[0]
                else:
                    return JsonResponse({'error': '介绍人不存在！'})
            
            user = User.objects.create(user_name=self.wx_num, nick_name=self.wx_nck, telephone=self.telephone, introducer=self.introducer)
            user.save()
            return JsonResponse({'msg': '恭喜您注册成功！'})     

    def existed(self):
        try:
            res = User.objects.get(user_name=self.wx_num)
            return True
        except ObjectDoesNotExist:
            return False

    def get(self, request, user_n):      
        user = User.objects.get(user_name=user_n)     
        ctx = {'uname': user.nick_name, 'uscore': user.score_nowithdraw+user.score_withdrawable}
        
        return render(request, 'user_info.html', context=ctx)

import json
import logging
import os
import requests

from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
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

def register(request, _):
    """
     `` request `` 请求对象
    """
    return render(request, 'register.html')


def existed(openid):
    try:
        res = User.objects.get(user_name=openid)
        return True
    except ObjectDoesNotExist:
        return False


def get_accesstoken(request):
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
        user = User.objects.get(user_name=openid)     
        ctx = {'uname': user.nick_name, 'uscore': user.score_nowithdraw+user.score_withdrawable}      
        return render(request, 'user_info.html', context=ctx)
    else:
        # 获取用户资料
        url = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN'.format(access_token, openid)
        response = requests.get(url)
        responsedict = json.loads(response.text)
        logger.info(response.text)
        
        return JsonResponse(render_to_string('register.html', context=responsedict), safe=False)


class UserView(View):
    openid = ''
    nickname = ''
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

            self.openid = body["wx_num"]
            self.nickname = body["wx_nck"]
            self.telephone = body['telephone']
            self.introducer = body['intro']
        except:
            return JsonResponse({'error': '哦吼，网络开小差了！'})  
            
        if self.introducer == '':
            self.introducer = None
        else:             
            res1 = User.objects.filter(telephone=self.introducer)
            if res1.exists():
                self.introducer = res1[0]
            else:
                return JsonResponse({'error': '介绍人不存在！'})
            # nickname = response['nickname']
            # sex = response['sex']
            # province = response['province']
            # city = response['city']
            # country = response['country']
            # headimgurl = response['headimgurl']
        
        user = User.objects.create(user_name=self.wx_num, nick_name=self.wx_nck, telephone=self.telephone, introducer=self.introducer)
        user.save()
        return JsonResponse({'msg': '恭喜您注册成功！'})     

    

    
import json
import logging

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from qzkj.models import User
from django.core.exceptions import ObjectDoesNotExist
import requests
from qzkj.settings import BASE_DIR

logger = logging.getLogger('log')


def verify(request):
    with open(settings.BASE_DIR + 'MP_verify_yxSL8Vl2Cy7VfcHP.txt', 'r') as f:
        str = f.readline()
    return HttpResponse(str)

def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """
    return render(request, 'index.html')


def wxuser_auth(request, _):
    print(request)
    url = "http://api.weixin.qq.com/sns/userinfo?openid="+request.headers['x-wx-openid']
    response = requests.get(url)
    print(response)
    return JsonResponse(response)


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


# def counter(request, _):
#     """
#     获取当前计数

#      `` request `` 请求对象
#     """

#     rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
#     if request.method == 'GET' or request.method == 'get':
#         rsp = get_count()
#     elif request.method == 'POST' or request.method == 'post':
#         rsp = update_count(request)
#     else:
#         rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
#                             json_dumps_params={'ensure_ascii': False})
#     logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
#     return rsp


# def get_count():
#     """
#     获取当前计数
#     """

#     try:
#         data = Counters.objects.get(id=1)
#     except Counters.DoesNotExist:
#         return JsonResponse({'code': 0, 'data': 0},
#                     json_dumps_params={'ensure_ascii': False})
#     return JsonResponse({'code': 0, 'data': data.count},
#                         json_dumps_params={'ensure_ascii': False})


# def update_count(request):
#     """
#     更新计数，自增或者清零

#     `` request `` 请求对象
#     """

#     logger.info('update_count req: {}'.format(request.body))

#     body_unicode = request.body.decode('utf-8')
#     body = json.loads(body_unicode)

#     if 'action' not in body:
#         return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
#                             json_dumps_params={'ensure_ascii': False})

#     if body['action'] == 'inc':
#         try:
#             data = Counters.objects.get(id=1)
#         except Counters.DoesNotExist:
#             data = Counters()
#         data.id = 1
#         data.count += 1
#         data.save()
#         return JsonResponse({'code': 0, "data": data.count},
#                     json_dumps_params={'ensure_ascii': False})
#     elif body['action'] == 'clear':
#         try:
#             data = Counters.objects.get(id=1)
#             data.delete()
#         except Counters.DoesNotExist:
#             logger.info('record not exist')
#         return JsonResponse({'code': 0, 'data': 0},
#                     json_dumps_params={'ensure_ascii': False})
#     else:
#         return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
#                     json_dumps_params={'ensure_ascii': False})

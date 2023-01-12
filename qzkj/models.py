from django.db import models


# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=200, primary_key=True, verbose_name='微信id')
    nick_name = models.CharField(max_length=200, blank=True, verbose_name='微信昵称')
    telephone = models.CharField(max_length=20, null=False, blank=False, verbose_name='手机号')
    introducer= models.ForeignKey('self', null=True, default=None, on_delete=models.SET_DEFAULT, verbose_name='介绍人')
    score_nowithdraw = models.IntegerField(default=0, verbose_name='不可提现积分')
    score_withdrawable = models.IntegerField(default=0 , verbose_name='可提现积分')

    class Meta:
        verbose_name_plural = '芪尊用户'
        db_table = 'User'

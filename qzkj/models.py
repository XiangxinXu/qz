from django.db import models


# Create your models here.
class User(models.Model):
    openid = models.CharField(max_length=200, primary_key=True, verbose_name='微信id')
    nick_name = models.CharField(max_length=200, blank=True, verbose_name='微信昵称')
    telephone = models.CharField(max_length=20, null=False, blank=False, verbose_name='手机号')
    introducer= models.ForeignKey('self', null=True, default=None, on_delete=models.SET_DEFAULT, verbose_name='介绍人')
    score_nowithdraw = models.IntegerField(default=0, verbose_name='不可提现积分')
    score_withdrawable = models.IntegerField(default=0 , verbose_name='可提现积分')

    class Meta:
        verbose_name_plural = '芪尊用户'
        db_table = 'User'

class ScoreChangeLog(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True, verbose_name='微信id')
    openid= models.ForeignKey(User,null=False, default="", on_delete=models.CASCADE, verbose_name='微信id')
    change_datetime = models.DateTimeField(auto_now=True, verbose_name='时间')
    score_change = models.IntegerField(default=0, verbose_name='积分变动')

    class ScoreTypeChoices(models.TextChoices):
        BOTH = 'both'
        NO = 'nowithdraw'
        WI = 'withdrawable'
    score_type = models.CharField(max_length=15, choices = ScoreTypeChoices.choices, verbose_name='可否提现')

    class Meta:
        verbose_name_plural = '积分变动详情'
        db_table = 'ScoreChangeLog'

    def get_score_type(self):
        if self.score_type == self.ScoreTypeChoices.BOTH:
            return '混合积分'
        elif self.score_type == self.ScoreTypeChoices.NO:
            return '不可提现积分'
        else:
            return '可提现积分'
    get_score_type.short_description = '积分形式'

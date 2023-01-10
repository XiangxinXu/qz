from django.db import models


# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=200, primary_key=True)
    nick_name = models.CharField(max_length=200, blank=True)
    telephone = models.CharField(max_length=20, null=False, blank=False)
    introducer= models.ForeignKey('self', null=True, default=None, on_delete=models.SET_DEFAULT)
    score_nowithdraw = models.IntegerField(default=0)
    score_withdrawable = models.IntegerField(default=0)

    class Meta:
        db_table = 'User'

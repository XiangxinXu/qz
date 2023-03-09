from django.contrib import admin
from .models import User
from .models import ScoreChangeLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nick_name', 'telephone', 'openid', 'introducer', 'score_nowithdraw', 'score_withdrawable')
    readonly_fields = ('user_name', 'nick_name', 'telephone', 'introducer',)
    search_fields = ('nick_name', 'telephone')

    
@admin.register(ScoreChangeLog)
class ScoreChangeLogAdmin(admin.ModelAdmin):
    list_display = ('openid', 'score_type')


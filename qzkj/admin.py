from django.contrib import admin
from .models import User
from .models import ScoreChangeLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nick_name', 'telephone', 'openid', 'introducer', 'score_nowithdraw', 'score_withdrawable')
    readonly_fields = ('openid', 'nick_name', 'telephone', 'introducer',)
    search_fields = ('nick_name', 'telephone')

    
@admin.register(ScoreChangeLog)
class ScoreChangeLogAdmin(admin.ModelAdmin):
    list_display = ('openid', 'change_datetime', 'score_change', 'get_score_type')
    readonly_fields = ('openid', 'change_datetime', 'score_change', 'get_score_type')
    list_display_links = None




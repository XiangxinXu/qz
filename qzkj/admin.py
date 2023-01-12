from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nick_name', 'telephone', 'user_name', 'introducer', 'score_nowithdraw', 'score_withdrawable')
    readonly_fields = ('user_name', 'nick_name', 'telephone', 'introducer',)
    search_fields = ('nick_name', 'telephone')

    

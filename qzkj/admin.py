from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('user_name','nick_name', 'telephone', 'introducer',)
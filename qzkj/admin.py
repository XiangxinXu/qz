from django.contrib import admin
from .models import User
from .models import ScoreChangeLog


admin.site.site_header = '芪尊科技后台管理系统'
admin.site.site_title = '芪尊科技后台管理系统'
admin.site.index_title = '芪尊科技后台管理系统'

class ExportCsvMixin:
    '''导出csv'''
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = "导出csv"


@admin.register(User)
class UserAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('nick_name', 'telephone', 'openid', 'introducer', 'score_nowithdraw', 'score_withdrawable')
    readonly_fields = ('openid', 'nick_name', 'telephone', 'introducer',)
    search_fields = ('nick_name', 'telephone')
    actions = ["export_as_csv"]

    
@admin.register(ScoreChangeLog)
class ScoreChangeLogAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('openid', 'change_datetime', 'score_change', 'get_score_type')
    readonly_fields = ('openid', 'change_datetime', 'score_change', 'get_score_type')
    list_display_links = None
    actions = ["export_as_csv"]




from django.contrib import admin

from .models import GenresParams, MailTemplate, MonthlyParams


# @admin.register(GenresParams)
# class GenresParamsAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(MonthlyParams)
# class MonthlyParamsAdmin(admin.ModelAdmin):
#     pass


@admin.register(MailTemplate)
class MailTemplateAdmin(admin.ModelAdmin):
    pass
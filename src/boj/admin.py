from django.contrib import admin

from boj.models import *


@admin.register(BOJUser)
class BOJUserAdmin(admin.ModelAdmin):
    pass


@admin.register(BOJTag)
class BOJTagAdmin(admin.ModelAdmin):
    pass

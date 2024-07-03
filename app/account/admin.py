from django.contrib import admin

from account.models import *


@admin.register(User)
class AccountAdmin(admin.ModelAdmin):
    pass

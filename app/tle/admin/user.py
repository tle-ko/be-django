from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tle.models import User


@admin.register(User)
class UserModelAdmin(UserAdmin):
    fieldsets = [
        (None, {'fields': [
            User.field_name.EMAIL,
            User.field_name.USERNAME,
            User.field_name.PASSWORD,
            User.field_name.PROFILE_IMAGE,
            User.field_name.BOJ_USERNAME,
            User.field_name.BOJ_LEVEL,
            User.field_name.BOJ_LEVEL_UPDATED_AT,
            User.field_name.IS_ACTIVE,
            User.field_name.IS_STAFF,
            User.field_name.IS_SUPERUSER,
            User.field_name.CREATED_AT,
        ]}),
    ]

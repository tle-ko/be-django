from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tle.models import User


@admin.register(User)
class UserModelAdmin(UserAdmin):
    fieldsets = [
        *UserAdmin.fieldsets,
        (None, {'fields': [
            'profile_image',
            'boj_username',
            'boj_tier',
            'boj_tier_updated_at',
        ]}),
    ]

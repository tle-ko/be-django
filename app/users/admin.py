from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User
from users.models import UserEmailVerification


admin.site.register([
    UserEmailVerification,
])


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = None
    list_display = [
        User.field_name.USERNAME,
        User.field_name.EMAIL,
        User.field_name.BOJ_USERNAME,
        User.field_name.IS_ACTIVE,
        User.field_name.IS_STAFF,
        User.field_name.IS_SUPERUSER,
        User.field_name.CREATED_AT,
    ]

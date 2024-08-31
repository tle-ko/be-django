from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User
from users.models import UserEmailVerification


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


@admin.register(UserEmailVerification)
class UserEmailVerificationModelAdmin(admin.ModelAdmin):
    list_display = [
        UserEmailVerification.field_name.EMAIL,
        UserEmailVerification.field_name.VERIFICATION_CODE,
        UserEmailVerification.field_name.VERIFICATION_TOKEN,
        UserEmailVerification.field_name.EXPIRES_AT,
    ]

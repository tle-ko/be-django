from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import QuerySet
from django.utils.html import format_html

from . import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    fieldsets = None
    list_display = [
        'get_profile_image',
        models.User.field_name.PK,
        models.User.field_name.USERNAME,
        models.User.field_name.EMAIL,
        models.User.field_name.BOJ_USERNAME,
        'get_boj_level',
        models.User.field_name.IS_ACTIVE,
        models.User.field_name.IS_STAFF,
        models.User.field_name.IS_SUPERUSER,
        models.User.field_name.CREATED_AT,
    ]
    actions = [
        'action_boj_update',
        'action_boj_update_async',
    ]

    @admin.display(description='Image')
    def get_profile_image(self, obj: models.User):
        return format_html(f'<img src="{obj.get_profile_image_url()}" width="50" height="50" />')

    @admin.display(description='BOJ Level')
    def get_boj_level(self, obj: models.User):
        return obj.get_boj_level().get_name()

    @admin.action(description="Update selected Users' BOJ data. (via solved.ac API)")
    def action_boj_update(self, request, queryset: QuerySet[models.User]):
        for obj in queryset:
            obj.get_boj_user().update()

    @admin.action(description="Schedule an update for selected Users' BOJ data. (via solved.ac API)")
    def action_boj_update_async(self, request, queryset: QuerySet[models.User]):
        for obj in queryset:
            obj.get_boj_user().update_async()


@admin.register(models.UserEmailVerification)
class UserEmailVerificationModelAdmin(admin.ModelAdmin):
    list_display = [
        models.UserEmailVerification.field_name.EMAIL,
        models.UserEmailVerification.field_name.VERIFICATION_CODE,
        models.UserEmailVerification.field_name.VERIFICATION_TOKEN,
        models.UserEmailVerification.field_name.EXPIRES_AT,
    ]

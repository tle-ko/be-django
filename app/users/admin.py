from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User, UserEmailVerification
from crews.models import CrewMember


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
        'get_crews',
        User.field_name.IS_ACTIVE,
        User.field_name.IS_STAFF,
        User.field_name.IS_SUPERUSER,
        User.field_name.CREATED_AT,
    ]

    @admin.display(description='captains / members')
    def get_crews(self, user: User) -> str:
        n_captains = CrewMember.objects.filter(**{
            CrewMember.field_name.USER: user,
            CrewMember.field_name.IS_CAPTAIN: True,
        }).count()
        n_members = CrewMember.objects.filter(**{
            CrewMember.field_name.USER: user,
        }).count()
        return f'{n_captains} / {n_members}'

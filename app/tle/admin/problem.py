from django.contrib import admin, messages
from django.utils.translation import ngettext

from tle.models import Problem


@admin.register(Problem)
class ProblemModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'updated_at']
    list_filter = ['created_by', 'created_at', 'updated_at']
    search_fields = ['title', 'created_by__username']
    ordering = ['-created_at']
    actions = ['set_creator']

    @admin.action(description="set 'created_by' of selected problems to current user")
    def set_creator(self, request, queryset):
        user = request.user
        updated = queryset.update(created_by=user)
        self.message_user(
            request,
            ngettext(
                "%d story was successfully marked as published.",
                "%d stories were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib import admin
from apps.background_task.models import Task
from apps.background_task.models import CompletedTask


def inc_priority(modeladmin, request, queryset):
    for obj in queryset:
        obj.priority += 1
        obj.save()
inc_priority.short_description = "priority += 1"

def dec_priority(modeladmin, request, queryset):
    for obj in queryset:
        obj.priority -= 1
        obj.save()
dec_priority.short_description = "priority -= 1"

def reschedule_now(modeladmin, request, queryset):
    for obj in queryset:
        obj.run_at = datetime.now()
        obj.save()

class TaskAdmin(admin.ModelAdmin):
    display_filter = ['task_name']
    search_fields = ['task_name', 'task_params', ]
    list_display = ['task_name', 'task_params', 'run_at', 'priority', 'attempts', 'has_error', 'locked_by', 'locked_by_pid_running', ]
    actions = [inc_priority, dec_priority, reschedule_now]

class CompletedTaskAdmin(admin.ModelAdmin):
    display_filter = ['task_name']
    search_fields = ['task_name', 'task_params', ]
    list_display = ['task_name', 'task_params', 'run_at', 'priority', 'attempts', 'has_error', 'locked_by', 'locked_by_pid_running', ]


admin.site.register(Task, TaskAdmin)
admin.site.register(CompletedTask, CompletedTaskAdmin)

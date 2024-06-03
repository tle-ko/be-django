from django.contrib import admin

from crew.models import *


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    pass


@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    pass


@admin.register(CrewMemberRequest)
class CrewMemberRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(CrewActivity)
class CrewActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(CrewActivityProblem)
class CrewActivityProblemAdmin(admin.ModelAdmin):
    pass


@admin.register(CrewActivityProblemSubmission)
class CrewActivityProblemSubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(CrewActivityProblemSubmissionComment)
class CrewActivityProblemSubmissionCommentAdmin(admin.ModelAdmin):
    pass

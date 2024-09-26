from django.contrib import admin

from users.models import User

from . import models


@admin.register(models.CrewDAO)
class CrewModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewDAO.method_name.GET_DISPLAY_NAME,
        models.CrewDAO.field_name.PK,
        models.CrewDAO.field_name.IS_ACTIVE,
        models.CrewDAO.field_name.IS_RECRUITING,
        models.CrewDAO.field_name.CREATED_AT,
    ]
    search_fields = [
        models.CrewDAO.field_name.NAME,
        models.CrewDAO.field_name.CREATED_BY+'__'+User.field_name.USERNAME,
        models.CrewDAO.field_name.ICON,
    ]


@admin.register(models.CrewMemberDAO)
class CrewMemberModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewMemberDAO.field_name.USER,
        models.CrewMemberDAO.field_name.CREW,
        models.CrewMemberDAO.field_name.IS_CAPTAIN,
        models.CrewMemberDAO.field_name.CREATED_AT,
    ]
    search_fields = [
        models.CrewMemberDAO.field_name.CREW+'__'+models.CrewDAO.field_name.NAME,
        models.CrewMemberDAO.field_name.USER+'__'+User.field_name.USERNAME,
    ]
    ordering = [
        models.CrewMemberDAO.field_name.CREW,
        models.CrewMemberDAO.field_name.IS_CAPTAIN,
    ]


@admin.register(models.CrewSubmittableLanguageDAO)
class CrewSubmittableLanguageModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewSubmittableLanguageDAO.field_name.CREW,
        models.CrewSubmittableLanguageDAO.field_name.LANGUAGE,
    ]
    search_fields = [
        models.CrewSubmittableLanguageDAO.field_name.CREW+'__'+models.CrewDAO.field_name.NAME,
        models.CrewSubmittableLanguageDAO.field_name.LANGUAGE,
    ]
    ordering = [
        models.CrewSubmittableLanguageDAO.field_name.CREW,
        models.CrewSubmittableLanguageDAO.field_name.LANGUAGE,
    ]

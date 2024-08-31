# Generated by Django 4.2.13 on 2024-09-01 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BOJProblem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.TextField()),
                ("description", models.TextField()),
                ("input_description", models.TextField()),
                ("output_description", models.TextField()),
                ("memory_limit", models.FloatField()),
                ("time_limit", models.FloatField()),
                ("tags", models.JSONField(default=list)),
                (
                    "level",
                    models.IntegerField(
                        choices=[
                            (0, "Unrated"),
                            (1, "브론즈 5"),
                            (2, "브론즈 4"),
                            (3, "브론즈 3"),
                            (4, "브론즈 2"),
                            (5, "브론즈 1"),
                            (6, "실버 5"),
                            (7, "실버 4"),
                            (8, "실버 3"),
                            (9, "실버 2"),
                            (10, "실버 1"),
                            (11, "골드 5"),
                            (12, "골드 4"),
                            (13, "골드 3"),
                            (14, "골드 2"),
                            (15, "골드 1"),
                            (16, "플래티넘 5"),
                            (17, "플래티넘 4"),
                            (18, "플래티넘 3"),
                            (19, "플래티넘 2"),
                            (20, "플래티넘 1"),
                            (21, "다이아몬드 5"),
                            (22, "다이아몬드 4"),
                            (23, "다이아몬드 3"),
                            (24, "다이아몬드 2"),
                            (25, "다이아몬드 1"),
                            (26, "루비 5"),
                            (27, "루비 4"),
                            (28, "루비 3"),
                            (29, "루비 2"),
                            (30, "루비 1"),
                            (31, "마스터"),
                        ]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BOJUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "username",
                    models.TextField(help_text="백준 아이디", max_length=40, unique=True),
                ),
                (
                    "level",
                    models.IntegerField(
                        choices=[
                            (0, "Unrated"),
                            (1, "브론즈 5"),
                            (2, "브론즈 4"),
                            (3, "브론즈 3"),
                            (4, "브론즈 2"),
                            (5, "브론즈 1"),
                            (6, "실버 5"),
                            (7, "실버 4"),
                            (8, "실버 3"),
                            (9, "실버 2"),
                            (10, "실버 1"),
                            (11, "골드 5"),
                            (12, "골드 4"),
                            (13, "골드 3"),
                            (14, "골드 2"),
                            (15, "골드 1"),
                            (16, "플래티넘 5"),
                            (17, "플래티넘 4"),
                            (18, "플래티넘 3"),
                            (19, "플래티넘 2"),
                            (20, "플래티넘 1"),
                            (21, "다이아몬드 5"),
                            (22, "다이아몬드 4"),
                            (23, "다이아몬드 3"),
                            (24, "다이아몬드 2"),
                            (25, "다이아몬드 1"),
                            (26, "루비 5"),
                            (27, "루비 4"),
                            (28, "루비 3"),
                            (29, "루비 2"),
                            (30, "루비 1"),
                            (31, "마스터"),
                        ],
                        default=0,
                    ),
                ),
                ("rating", models.IntegerField(default=0)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="BOJUserSnapshot",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "level",
                    models.IntegerField(
                        choices=[
                            (0, "Unrated"),
                            (1, "브론즈 5"),
                            (2, "브론즈 4"),
                            (3, "브론즈 3"),
                            (4, "브론즈 2"),
                            (5, "브론즈 1"),
                            (6, "실버 5"),
                            (7, "실버 4"),
                            (8, "실버 3"),
                            (9, "실버 2"),
                            (10, "실버 1"),
                            (11, "골드 5"),
                            (12, "골드 4"),
                            (13, "골드 3"),
                            (14, "골드 2"),
                            (15, "골드 1"),
                            (16, "플래티넘 5"),
                            (17, "플래티넘 4"),
                            (18, "플래티넘 3"),
                            (19, "플래티넘 2"),
                            (20, "플래티넘 1"),
                            (21, "다이아몬드 5"),
                            (22, "다이아몬드 4"),
                            (23, "다이아몬드 3"),
                            (24, "다이아몬드 2"),
                            (25, "다이아몬드 1"),
                            (26, "루비 5"),
                            (27, "루비 4"),
                            (28, "루비 3"),
                            (29, "루비 2"),
                            (30, "루비 1"),
                            (31, "마스터"),
                        ]
                    ),
                ),
                ("rating", models.IntegerField()),
                ("created_at", models.DateTimeField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="boj.bojuser"
                    ),
                ),
            ],
        ),
    ]

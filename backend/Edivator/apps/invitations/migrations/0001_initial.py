# Generated by Django 4.2.13 on 2024-07-15 07:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invitation",
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
                    "token",
                    models.CharField(max_length=255, unique=True, verbose_name="邀请码"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="创建时间"
                    ),
                ),
                ("expires_at", models.DateTimeField(verbose_name="过期时间")),
                (
                    "is_accepted",
                    models.BooleanField(default=False, verbose_name="是否已接受"),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invitations",
                        to="companies.company",
                        verbose_name="企业",
                    ),
                ),
            ],
            options={
                "verbose_name": "邀请码",
                "verbose_name_plural": "邀请码列表",
                "db_table": "invitations",
            },
        ),
    ]
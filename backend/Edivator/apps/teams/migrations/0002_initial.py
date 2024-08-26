# Generated by Django 4.2.13 on 2024-07-15 07:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("teams", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="users",
            field=models.ManyToManyField(
                blank=True,
                related_name="affiliated_teams",
                to=settings.AUTH_USER_MODEL,
                verbose_name="团队所属的企业",
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notifications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="applicant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sent_requests",
                to=settings.AUTH_USER_MODEL,
                verbose_name="申请人",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="team_requests",
                to="teams.team",
                verbose_name="申请的团队",
            ),
        ),
    ]

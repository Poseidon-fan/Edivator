# Generated by Django 4.2.13 on 2024-07-17 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0003_alter_template_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="Keyword",
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
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "keywords",
            },
        ),
        migrations.AddField(
            model_name="document",
            name="keywords",
            field=models.ManyToManyField(
                related_name="documents", to="documents.keyword"
            ),
        ),
    ]

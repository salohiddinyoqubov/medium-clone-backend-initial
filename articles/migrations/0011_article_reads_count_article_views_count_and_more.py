# Generated by Django 4.2.14 on 2024-11-24 07:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("articles", "0010_alter_topic_options_alter_topic_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="reads_count",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name="article",
            name="views_count",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="status",
            field=models.CharField(
                choices=[("pending", "Pending"), ("publish", "Publish")],
                default="pending",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="Clap",
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
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="articles.article",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Clap",
                "verbose_name_plural": "Claps",
            },
        ),
    ]

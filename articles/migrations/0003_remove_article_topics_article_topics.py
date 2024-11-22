# Generated by Django 4.2.14 on 2024-11-21 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0002_rename_topic_article_topics"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="topics",
        ),
        migrations.AddField(
            model_name="article",
            name="topics",
            field=models.ManyToManyField(related_name="topics", to="articles.topic"),
        ),
    ]

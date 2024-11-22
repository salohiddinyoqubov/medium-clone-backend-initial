# Generated by Django 4.2.14 on 2024-11-22 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0004_alter_article_topics"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="thumbnail",
            field=models.ImageField(blank=True, upload_to="thumbnail/"),
        ),
        migrations.AlterField(
            model_name="article",
            name="topics",
            field=models.ManyToManyField(related_name="topics", to="articles.topic"),
        ),
    ]
# Generated by Django 4.2.14 on 2024-11-22 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0006_alter_article_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={},
        ),
        migrations.AlterModelTable(
            name="article",
            table="article",
        ),
    ]
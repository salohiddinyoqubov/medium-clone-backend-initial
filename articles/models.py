from ckeditor.fields import RichTextField
from django.db import models

from users.models import CustomUser


class Topic(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "topic"
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        ordering = ["name"]


# Create your models here.
class Article(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PUBLISH = "publish", "Publish"
        TRASH = "trash", "Trash"

    title = models.CharField(max_length=255)
    summary = models.TextField()
    content = RichTextField()
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    thumbnail = models.ImageField(upload_to="thumbnail/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic, related_name="topics")
    views_count = models.IntegerField(null=True, default=0)
    reads_count = models.IntegerField(null=True, default=0)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = "article"
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["-created_at"]


class Clap(models.Model):
    article = models.ForeignKey(
        to=Article, on_delete=models.CASCADE, related_name="claps"
    )
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Clap"
        verbose_name_plural = "Claps"

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = RichTextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comment"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]


class TopicFollow(models.Model):
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="topic"
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="follow_user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "follow"
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
        ordering = ["-created_at"]

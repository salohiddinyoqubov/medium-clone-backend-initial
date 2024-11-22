from tabnanny import verbose

from django.db import models

from users.models import CustomUser


class Topic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
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
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    title = models.CharField(max_length=255)
    summary = models.TextField()
    content = models.TextField()
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    thumbnail = models.ImageField(upload_to="thumbnail/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic, related_name="topics")

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = "article"
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["-created_at"]

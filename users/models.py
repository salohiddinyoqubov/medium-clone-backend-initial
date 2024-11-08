import os
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django_resized import ResizedImageField


def file_upload(instance, filename):
    """This function is used to upload the user's avatar."""
    ext = filename.split(".")[-1]
    filename = f"{instance.username}.{ext}"
    return os.path.join("users/avatars/", filename)


class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = ResizedImageField(
        size=[300, 300], crop=["top", "left"], upload_to=file_upload, blank=True
    )

    class Meta:
        db_table = "user"  # database table name
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]  # descending order by date joined

    def __str__(self):
        """This method returns the full name of the user"""
        if self.full_name:
            return self.full_name
        else:
            return self.email or self.username

    @property
    def full_name(self):
        """Returns the user's full name."""
        return f"{self.last_name} {self.first_name} {self.middle_name}"

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django_extensions.db.models import (
    TimeStampedModel,
    TitleSlugDescriptionModel,
    TitleDescriptionModel,
)
from courses.fields import OrderField

# Get the user model to link to the owner field
User = get_user_model()


class Subject(TitleSlugDescriptionModel, TimeStampedModel):
    pass


# Course Model
class Course(TitleSlugDescriptionModel, TimeStampedModel):
    owner = models.ForeignKey(
        User,
        related_name="courses_created",
        on_delete=models.CASCADE,
    )
    subject = models.ForeignKey(
        Subject,
        related_name="courses",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="courses/%Y/%m/%d")
    duration = models.CharField(max_length=96, null=True, blank=True)
    fees = models.DecimalField(max_digits=12, decimal_places=2)
    level = models.CharField(max_length=96, null=True, blank=True)
    instructor_based = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# Module Model
class Module(TitleDescriptionModel):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    order = OrderField(blank=True, for_fields=["course"])

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Module {self.order + 1}: {self.title}"


# Content Model (Generic relation to the specific content types)
class Content(TimeStampedModel):
    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    order = OrderField(blank=True, for_fields=["module"])

    class Meta:
        ordering = ["id"]


# Text Model for storing text-based content
class Text(models.Model):
    owner = models.ForeignKey(
        User, related_name="texts_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.content


# Video Model for storing video links (e.g., YouTube, Vimeo)
class Video(models.Model):
    owner = models.ForeignKey(
        User, related_name="videos_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    url = models.URLField()  # URL to the video (e.g., YouTube URL)

    def __str__(self):
        return self.title


# Image Model for storing images
class Image(models.Model):
    owner = models.ForeignKey(
        User, related_name="images_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    file = models.ImageField(upload_to="images/%Y/%m/%d/")  # Image file upload

    def __str__(self):
        return self.title


# File Model for storing downloadable files (e.g., PDFs, documents)
class File(models.Model):
    owner = models.ForeignKey(
        User, related_name="files_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="files/%Y/%m/%d/")  # File upload (e.g., PDFs)

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Get the user model to link to the owner field
User = get_user_model()


# Course Model
class Course(models.Model):
    owner = models.ForeignKey(
        User, related_name="courses_created", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Module Model
class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)  # Order of the module in the course

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Module {self.order + 1}: {self.title}"


# Content Model (Generic relation to the specific content types)
class Content(models.Model):
    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["id"]


# Text Model for storing text-based content
class Text(models.Model):
    owner = models.ForeignKey(
        User, related_name="text_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.content


# Video Model for storing video links (e.g., YouTube, Vimeo)
class Video(models.Model):
    owner = models.ForeignKey(
        User, related_name="video_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    url = models.URLField()  # URL to the video (e.g., YouTube URL)

    def __str__(self):
        return self.title


# Image Model for storing images
class Image(models.Model):
    owner = models.ForeignKey(
        User, related_name="image_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    file = models.ImageField(upload_to="images")  # Image file upload

    def __str__(self):
        return self.title


# File Model for storing downloadable files (e.g., PDFs, documents)
class File(models.Model):
    owner = models.ForeignKey(
        User, related_name="file_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="files")  # File upload (e.g., PDFs)

    def __str__(self):
        return self.title

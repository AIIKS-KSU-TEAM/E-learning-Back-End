from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from django.utils.text import slugify

User = get_user_model()


class Subject(TimeStampedModel):
    name = models.CharField(max_length=224)
    slug = models.SlugField(max_length=224, unique=True)
    description = models.TextField()

    def save(self, **kwargs):

        if not self.slug:

            base_slug = slugify(self.name)

            slug = base_slug
            counter = 1

            while Subject.objects.filter(slug=slug):
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        return super().save(**kwargs)

    def __str__(self):
        return self.name


class Course(TimeStampedModel, TitleSlugDescriptionModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="courses",
    )
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/")
    duration = models.CharField(max_length=224, blank=True, null=True)
    fees = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    level = models.CharField(max_length=224, blank=True, null=True)
    instructor_based = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class ContentType(models.TextChoices):
    VIDEO = "video", "Video"
    FILE = "file", "File"
    IMAGE = "image", "Image"
    TEXT = "text", "Text"


class Content(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="contents"
    )
    content_type = models.CharField(max_length=50, choices=ContentType.choices)
    content = models.TextField()

    def __str__(self):
        return f"{self.content_type}: {self.content[:20]}..."


class Assignment(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="assignments"
    )
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="assignments/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

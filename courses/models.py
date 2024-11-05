from django.db import models
from django.conf import settings

class Subject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class ContentType(models.TextChoices):
    VIDEO = 'video', 'Video'
    FILE = 'file', 'File'
    IMAGE = 'image', 'Image'
    TEXT = 'text', 'Text'


class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=50, choices=ContentType.choices)
    content = models.TextField()

    def __str__(self):
        return f'{self.content_type}: {self.content[:20]}...'

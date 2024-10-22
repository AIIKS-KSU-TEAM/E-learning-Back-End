from django.db import models
from courses.models import Course
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel

User = get_user_model()


class Group(TimeStampedModel):
    name = models.CharField(max_length=96, null=False, blank=False)
    course = models.ForeignKey(
        Course, null=True, on_delete=models.SET_NULL, related_name="course_groups"
    )
    instructor = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="instructor_groups"
    )
    start = models.DateField(null=True)
    end = models.DateField(null=True)
    enrollment_key = models.CharField(max_length=32, null=True, blank=True)
    active = models.BooleanField(default=False)


class Enrollment(TimeStampedModel):

    STATUS_FEES_CHOICES = {
        "not-paid": "Not Paid",
        "partially-paid": "Partially Paid",
        "fully-paid": "Fully Paid",
    }

    course = models.ForeignKey(
        Course,
        null=True,
        on_delete=models.SET_NULL,
        related_name="corse_enrollments",
    )
    student = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="student_enrollments",
    )

    instructor = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="instructor_enrollments",
    )

    group = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        related_name="group_enrollments",
    )

    enrollment_date = (models.DateField(),)

    total_fees = models.DecimalField(max_digits=12, decimal_places=2)

    paid_fess = models.DecimalField(max_digits=12, decimal_places=2)

    status_fees = models.CharField(
        max_length=32,
        choices=STATUS_FEES_CHOICES,
        default="not-paid",
    )

    completed = models.BooleanField(default=False)

    approved = models.BooleanField(default=False)


class Review(TimeStampedModel):
    RATING_CHOICES = {
        5: "Strongly Recommend",
        4: "Recommend",
        3: "Neutral",
        2: "Discourage",
        1: "Strongly Discourage",
    }
    student = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="student_reviews",
    )
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    rating = models.SmallIntegerField(max_length=1, choices=RATING_CHOICES)
    comment = models.TextField()


class Team(TimeStampedModel, TitleSlugDescriptionModel):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="group_teams",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course_teams",
    )

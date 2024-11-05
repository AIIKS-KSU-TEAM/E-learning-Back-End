from django.test import TestCase
from django.contrib.auth import get_user_model
from courses.models import Subject, Course

User = get_user_model()


class SubjectModelTest(TestCase):

    def test_slug_generation(self):
        subject = Subject.objects.create(
            name="Test Subject", description="A sample description"
        )
        self.assertEqual(subject.slug, "test-subject")

    def test_unique_slug_generation(self):
        subject1 = Subject.objects.create(
            name="Test Subject", description="First sample description"
        )
        subject2 = Subject.objects.create(
            name="Test Subject", description="Second sample description"
        )

        self.assertEqual(subject1.slug, "test-subject")
        self.assertNotEqual(subject1.slug, subject2.slug)
        self.assertTrue(subject2.slug.startswith("test-subject"))
        self.assertRegex(
            subject2.slug, r"^test-subject-\d+$"
        )  # Ensures a number suffix is added

    def test_slug_preservation_on_update(self):
        subject = Subject.objects.create(
            name="Another Subject", description="A sample description"
        )
        original_slug = subject.slug
        subject.name = "Updated Subject Name"
        subject.save()

        # Check if the slug remains the same after updating the name
        self.assertEqual(subject.slug, original_slug)


class CourseModelTest(TestCase):

    def setUp(self):
        user_data = self.get_user_data()
        self.user = User.objects.create_user(**user_data)
        self.subject = Subject.objects.create(
            name="Mathematics", description="A sample subject"
        )

    def test_course_creation(self):
        course = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title="Algebra 101",
            description="An introductory course on Algebra.",
            duration="10 hours",
            fees=99.99,
            level="Beginner",
            instructor_based=True,
        )
        self.assertEqual(course.owner, self.user)
        self.assertEqual(course.subject, self.subject)
        self.assertEqual(course.title, "Algebra 101")
        self.assertEqual(course.slug, "algebra-101")
        self.assertEqual(course.fees, 99.99)
        self.assertTrue(course.instructor_based)

    def test_default_fees(self):
        course = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title="Geometry Basics",
            description="Introduction to geometry.",
        )
        self.assertEqual(course.fees, 0.0)

    def test_related_courses_for_subject(self):
        course1 = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title="Algebra 101",
            description="An introductory course on Algebra.",
        )
        course2 = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title="Geometry Basics",
            description="Basics of geometry.",
        )
        self.assertIn(course1, self.subject.courses.all())
        self.assertIn(course2, self.subject.courses.all())

    def get_user_data(self):
        return {"name": "John Doe", "email": "jdoe@gmail.com", "password": "pa$$w0rd!"}

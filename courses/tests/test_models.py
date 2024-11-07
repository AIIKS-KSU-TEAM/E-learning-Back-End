from django.test import TestCase
from django.contrib.auth import get_user_model
from courses.models import Subject, Course, Module
from courses.models import Content, TextContentItem
from courses.models import FileContentItem, YoutubeVideoContentItem
from django.contrib.contenttypes.models import ContentType

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


class ModuleModelTest(TestCase):

    def setUp(self):
        user_data = self.get_user_data()
        self.user = User.objects.create_user(**user_data)
        self.subject = Subject.objects.create(
            name="Mathematics", description="A sample subject"
        )
        self.course = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title="Algebra 101",
            description="An introductory course on Algebra.",
        )

    def test_module_creation(self):
        module = Module.objects.create(
            course=self.course,
            title="Module 1: Introduction to Algebra",
            description="Basic concepts of Algebra.",
        )
        self.assertEqual(module.course, self.course)
        self.assertEqual(module.title, "Module 1: Introduction to Algebra")
        self.assertEqual(module.order, 1)

    def test_module_ordering_within_course(self):
        # Create multiple modules within the same course to check ordering
        module1 = Module.objects.create(
            course=self.course,
            title="Module 1: Introduction",
            description="Introduction to course.",
        )
        module2 = Module.objects.create(
            course=self.course,
            title="Module 2: Algebra Basics",
            description="Basic concepts of Algebra.",
        )

        # Verify ordering
        self.assertEqual(module1.order, 1)
        self.assertEqual(module2.order, 2)
        self.assertLess(module1.order, module2.order)

    def test_module_ordering_reset_for_different_courses(self):
        # Create another course and module to check order reset
        another_course = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title="Geometry Basics",
            description="Introduction to geometry.",
        )
        module1 = Module.objects.create(
            course=self.course,
            title="Module 1: Algebra Basics",
            description="Basic concepts of Algebra.",
        )
        module2 = Module.objects.create(
            course=another_course,
            title="Module 1: Geometry Introduction",
            description="Introduction to Geometry.",
        )

        # Check if order resets for each course
        self.assertEqual(module1.order, 1)
        self.assertEqual(module2.order, 1)

    def get_user_data(self):
        return {"name": "John Doe", "email": "jdoe@gmail.com", "password": "pa$$w0rd!"}


class ContentModelTest(TestCase):

    def setUp(self):
        # Create common user, subject, course, and module
        self.user = User.objects.create_user(
            name="Jane Doe", email="jdoe@gmail.com", password="pa$$w0rd!"
        )
        self.subject = Subject.objects.create(
            name="Mathematics", description="A sample subject"
        )
        self.course = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title="Algebra 101",
            description="An introductory course on Algebra.",
        )
        self.module = Module.objects.create(
            course=self.course,
            title="Module 1: Introduction to Algebra",
            description="Introduction to Algebra concepts.",
        )

    def test_text_content_item_creation(self):
        text_content = TextContentItem.objects.create(
            owner=self.user,
            title="Algebra Basics Text",
            description="Basic concepts of Algebra in text format.",
            text="This is an introduction to Algebra.",
        )
        content_type = ContentType.objects.get_for_model(TextContentItem)
        content = Content.objects.create(
            module=self.module,
            content_type=content_type,
            object_id=text_content.id,
            order=1,
        )
        self.assertEqual(content.item, text_content)
        self.assertEqual(content.module, self.module)
        self.assertEqual(content.order, 1)

    def test_file_content_item_creation(self):
        file_content = FileContentItem.objects.create(
            owner=self.user,
            title="Algebra Worksheet",
            description="Worksheet for Algebra basics.",
            file="path/to/algebra_worksheet.pdf",
        )
        content_type = ContentType.objects.get_for_model(FileContentItem)
        content = Content.objects.create(
            module=self.module,
            content_type=content_type,
            object_id=file_content.id,
            order=2,
        )
        self.assertEqual(content.item, file_content)
        self.assertEqual(content.module, self.module)
        self.assertEqual(content.order, 2)

    def test_youtube_video_content_item_creation(self):
        youtube_video = YoutubeVideoContentItem.objects.create(
            owner=self.user,
            title="Algebra Introduction Video",
            description="A YouTube video introducing Algebra concepts.",
            url="https://www.youtube.com/watch?v=example",
        )
        content_type = ContentType.objects.get_for_model(YoutubeVideoContentItem)
        content = Content.objects.create(
            module=self.module,
            content_type=content_type,
            object_id=youtube_video.id,
            order=3,
        )
        self.assertEqual(content.item, youtube_video)
        self.assertEqual(content.module, self.module)
        self.assertEqual(content.order, 3)

    def test_content_ordering_within_module(self):
        text_content = TextContentItem.objects.create(
            owner=self.user,
            title="Algebra Basics Text",
            description="Basic concepts of Algebra in text format.",
            text="This is an introduction to Algebra.",
        )
        file_content = FileContentItem.objects.create(
            owner=self.user,
            title="Algebra Worksheet",
            description="Worksheet for Algebra basics.",
            file="path/to/algebra_worksheet.pdf",
        )
        youtube_video = YoutubeVideoContentItem.objects.create(
            owner=self.user,
            title="Algebra Introduction Video",
            description="A YouTube video introducing Algebra concepts.",
            url="https://www.youtube.com/watch?v=example",
        )

        content_type_text = ContentType.objects.get_for_model(TextContentItem)
        content_type_file = ContentType.objects.get_for_model(FileContentItem)
        content_type_video = ContentType.objects.get_for_model(YoutubeVideoContentItem)

        # Create content items with explicit ordering
        Content.objects.create(
            module=self.module,
            content_type=content_type_text,
            object_id=text_content.id,
            order=1,
        )
        Content.objects.create(
            module=self.module,
            content_type=content_type_file,
            object_id=file_content.id,
            order=2,
        )
        Content.objects.create(
            module=self.module,
            content_type=content_type_video,
            object_id=youtube_video.id,
            order=3,
        )

        # Verify the order
        contents = list(self.module.contents.all())
        self.assertEqual(contents[0].item, text_content)
        self.assertEqual(contents[1].item, file_content)
        self.assertEqual(contents[2].item, youtube_video)

from django.test import TestCase
from courses.models import Subject, Course, Module
from courses.models import Content, Text, Image, File, Video
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.contenttypes.models import ContentType


User = get_user_model()


class SubjectModelTest(TestCase):
    def get_data(self):
        return {
            "title": "Programming",
            "description": "The best subject ever",
        }

    def test_creating_a_new_subject(self):

        data = self.get_data()

        subject = Subject.objects.create(**data)

        self.assertIsNotNone(subject)

        self.assertEquals(subject.title, data["title"])

        self.assertEquals(subject.description, data["description"])

        self.assertIsNotNone(subject.slug)


class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="John Doe",
            email="jdoe@gmail.com",
            password="pa$$w0rd!",
        )
        self.subject = Subject.objects.create(
            title="Mathematics",
            description="A subject about numbers and equations",
        )

    def test_create_course(self):
        payload = {
            "title": "Algebra 101",
            "description": "Basic Algebra concepts",
            "owner": self.user,
            "subject": self.subject,
            "image": SimpleUploadedFile(
                name="test_image.jpg", content=b"", content_type="image/jpeg"
            ),
            "duration": "6 weeks",
            "fees": 3100.00,
            "level": "Beginner",
        }

        course = Course.objects.create(**payload)
        self.assertEqual(course.title, payload["title"])
        self.assertEqual(course.owner, payload["owner"])
        self.assertEqual(course.subject, payload["subject"])
        self.assertEqual(course.fees, payload["fees"])
        self.assertTrue(course.image)


class ModuleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="John Doe",
            email="jdoe@gmail.com",
            password="pa$$w0rd!",
        )
        self.subject = Subject.objects.create(
            title="Mathematics", description="A subject about numbers and equations"
        )
        self.course = Course.objects.create(
            title="Algebra 101",
            description="Basic Algebra concepts",
            owner=self.user,
            subject=self.subject,
            fees=100.00,
        )

    def test_create_module(self):
        attributes = {
            "title": "Introduction",
            "description": "Intro to Algebra",
            "course": self.course,
            "order": 1,
        }
        module = Module.objects.create(**attributes)
        self.assertEqual(module.course, attributes["course"])
        self.assertEqual(module.title, attributes["title"])
        self.assertEqual(module.order, attributes["order"])


class ContentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="John Doe",
            email="jdoe@gmail.com",
            password="pa$$w0rd!",
        )
        self.subject = Subject.objects.create(
            title="Mathematics", description="A subject about numbers and equations"
        )
        self.course = Course.objects.create(
            title="Algebra 101",
            description="Basic Algebra concepts",
            owner=self.user,
            subject=self.subject,
            fees=100.00,
        )
        self.module = Module.objects.create(
            title="Introduction", description="Intro to Algebra", course=self.course
        )
        self.text = Text.objects.create(
            owner=self.user, 
            title="Text Content", 
            content="This is a text content."
        )
        self.content_type = ContentType.objects.get_for_model(self.text)

    def test_create_content(self):
        content = Content.objects.create(
            module=self.module,
            content_type=self.content_type,
            object_id=self.text.id,
            order=1,
        )
        self.assertEqual(content.module, self.module)
        self.assertEqual(content.content_type, self.content_type)
        self.assertEqual(content.item, self.text)


class TextModelTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            name="John Doe",
            email="jdoe@gmail.com",
            password="pa$$w0rd!",
        )

    def test_create_text(self):
        text = Text.objects.create(
            owner=self.user, title="Lesson 1", content="This is a text lesson."
        )
        self.assertEqual(text.owner, self.user)
        self.assertEqual(text.content, "This is a text lesson.")


class VideoModelTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            name="John Doe",
            email="jdoe@gmail.com",
            password="pa$$w0rd!",
        )

    def test_create_video(self):
        video = Video.objects.create(
            owner=self.user,
            title="Video Lesson 1",
            url="https://www.youtube.com/watch?v=123456",
        )
        self.assertEqual(video.owner, self.user)
        self.assertEqual(video.title, "Video Lesson 1")
        self.assertEqual(video.url, "https://www.youtube.com/watch?v=123456")


class ImageModelTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            name="John Doe",
            email="jdoe@gmail.com",
            password="pa$$w0rd!",
        )

    def test_create_image(self):
        image = Image.objects.create(
            owner=self.user,
            title="Sample Image",
            file=SimpleUploadedFile(
                name="test_image.jpg", content=b"", content_type="image/jpeg"
            ),
        )
        self.assertEqual(image.owner, self.user)
        self.assertEqual(image.title, "Sample Image")
        self.assertTrue(image.file)


class FileModelTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            name="John Doe",
            email="jdoe@gmail.com",
            password="pa$$w0rd!",
        )

    def test_create_file(self):
        file = File.objects.create(
            owner=self.user,
            title="Sample PDF",
            file=SimpleUploadedFile(
                name="test_file.pdf",
                content=b"%PDF-1.4",
                content_type="application/pdf",
            ),
        )
        self.assertEqual(file.owner, self.user)
        self.assertEqual(file.title, "Sample PDF")
        self.assertTrue(file.file)

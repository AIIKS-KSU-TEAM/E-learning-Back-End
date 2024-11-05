from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class TestInstructorApiEndpoints(APITestCase):

    def setUp(self):

        data = self.get_user_data()
        self.user = User.objects.create_user(**data)
        self.client.force_authenticate(user=self.user)

    def test_api_instructor_get_url(self):
        url = reverse("api-instructor")
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def get_user_data(self):
        return {"name": "John Doe", "email": "jdoe@gmail.com", "password": "pa$$w0rd!"}


class TestInstructorCoursesApiEndpoints(APITestCase):

    def setUp(self):

        data = self.get_user_data()
        self.user = User.objects.create_user(**data)
        self.client.force_authenticate(user=self.user)

    def test_api_instructor_courses_get_url(self):
        url = reverse("api-instructor-courses-list")
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def get_user_data(self):
        return {"name": "John Doe", "email": "jdoe@gmail.com", "password": "pa$$w0rd!"}

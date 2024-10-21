from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTest(APITestCase):

    def setUp(self):
        data = self.get_data()
        self.user = User.objects.create_user(**data)
        self.url = reverse("login")

    def test_authentication_with_valid_credentials(self):
        data = self.get_data()
        response = self.client.post(self.url, data, format="json")

        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the required keys are in the response
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertIn("token_type", response.data)
        self.assertIn("expires_in", response.data)

        # Check that the token_type is "Bearer"
        self.assertEqual(response.data["token_type"], "Bearer")

        # Check that expires_in is an integer (number of seconds)
        self.assertIsInstance(response.data["expires_in"], int)

    def test_authentication_with_invalid_credentials(self):
        # Test an unsuccessful login with invalid credentials
        data = {"email": "testuser@example.com", "password": "wrongpassword"}
        response = self.client.post(self.url, data, format="json")

        # Assert that the status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert that the response contains an error message
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.data["detail"],
            "No active account found with the given credentials",
        )

    def test_authentication_with_missing_fields(self):
        # Test when required fields are missing
        data = {"email": "testuser@example.com"}
        response = self.client.post(self.url, data, format="json")

        # Assert that the status code is 400 Bad Request due to missing password
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check for the error message about the missing field
        self.assertIn("password", response.data)

    def get_data(self):
        return {"name": "John Doe", "email": "jdoe@gmail.com", "password": "pa$$w0rd!"}


class RegistrationTest(APITestCase):

    def setUp(self):
        self.url = reverse("register")

    def test_registration_with_valid_data(self):
        # Test a successful registration
        data = self.get_data()
        response = self.client.post(self.url, data, format="json")

        # Assert that the status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the required keys are in the response
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertIn("token_type", response.data)

        # Verify that the token_type is "Bearer"
        self.assertEqual(response.data["token_type"], "Bearer")

        # Verify that the user was actually created
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_registration_with_missing_password(self):
        # Test registration with missing password field
        data = self.get_data()
        data.pop("password")
        response = self.client.post(self.url, data, format="json")

        # Assert that the status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check for the error message about the missing password
        self.assertIn("password", response.data)

    def test_registration_with_existing_email(self):
        # Create a user with the same email beforehand
        data = self.get_data()
        User.objects.create_user(**data)

        # Attempt to register with the same email
        response = self.client.post(self.url, data, format="json")

        # Assert that the status code is 400 Bad Request due to unique constraint
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check for the error message related to email uniqueness
        self.assertIn("email", response.data)

    def get_data(self):
        return {"name": "John Doe", "email": "jdoe@gmail.com", "password": "pa$$w0rd!"}

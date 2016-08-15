from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from django.contrib.auth.models import User
from api.models import Bucketlist, Item


class TestBase(APITestCase):
    """ Base configurations for the tests """

    # Get authentication token
    def get_token(self):
        """ Returns authentication token """
        url = reverse("login")
        self.user = {"username": "testuser",
                     "password": "testpassword"}
        response = self.client.post(url, data=self.user)
        token = str(response.data.get("token"))
        return token

    def setUp(self):
        # Add test user
        url = reverse("user-list")
        self.user = {"username": "testuser",
                     "email": "testuser@email.com",
                     "password": "testpassword"}
        self.client.post(url, data=self.user)

        # Add test bucket list
        url = reverse("bucketlist-list")
        self.bucketlist = {"title": "The List of Awesome",
                           "description": "Awesome things!",
                           "created_by": 1}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.get_token())
        self.client.post(url, data=self.bucketlist)

        # Add test bucket list item
        # url = reverse("bucketlist-items-list")
        # self.item = {"title": "Swim with dolphins",
        #              "description": "Swim with dolphins in Watamu",
        #              "bucketlist_id": 1,
        #              "created_by": 1}
        # self.client.post(url, data=self.item)


class TestAuth(TestBase):
    """ Test user registration and login """

    def test_registration(self):
        """ Test user registration """
        url = reverse("user-list")
        self.user = {"username": "testuser2",
                     "email": "testuser2@email.com",
                     "password": "testpassword"}
        response = self.client.post(url, data=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertTrue("testuser2" in response.data["username"])
        self.assertTrue("testuser2@email.com" in response.data["email"])

    def test_login(self):
        """ Test user login """
        url = reverse("login")
        self.user = {"username": "testuser",
                     "password": "testpassword"}
        response = self.client.post(url, data=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_credentials(self):
        """ Test that users cannot login with invalid credentials """
        # Invalid username
        url = reverse("login")
        self.user = {"username": "invalid",
                     "password": "testpassword"}
        response = self.client.post(url, data=self.user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Invalid password
        url = reverse("login")
        self.user = {"username": "testuser",
                     "password": "invalid"}
        response = self.client.post(url, data=self.user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestBucketlists(TestBase):
    """ Test operations on bucketlists """

    def test_no_token(self):
        """
        Test that user cannot add a bucket list without
        an authentication token
        """
        url = reverse("bucketlist-list")
        self.bucketlist = {"title": "The List of Awesome",
                           "description": "Awesome things I want to do",
                           "created_by": 1}
        self.client.credentials()
        response = self.client.post(url, data=self.bucketlist)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue("Authentication credentials were not provided"
                        in response.data["detail"])

    def test_invalid_token(self):
        """
        Test that user cannot add a bucket list with
        an invalid token
        """
        url = reverse("bucketlist-list")
        self.bucketlist = {"title": "The List of Awesome",
                           "description": "Awesome things I want to do",
                           "created_by": 1}
        invalid_token = "1234"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + invalid_token)
        response = self.client.post(url, data=self.bucketlist)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue("Invalid token" in response.data["detail"])

    def test_add_bucketlist(self):
        """ Test that user cannot add a bucket list """
        url = reverse("bucketlist-list")
        self.bucketlist = {"title": "Knowledge Goals",
                           "description": "Things to learn",
                           "created_by": 1}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.get_token())
        response = self.client.post(url, data=self.bucketlist)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bucketlist.objects.count(), 2)
        self.assertTrue("Knowledge Goals" in response.data["title"])
        self.assertTrue("Things to learn" in response.data["description"])


class TestItems(TestBase):
    """ Test operations on bucket list items"""

    def setUp(self):
        pass

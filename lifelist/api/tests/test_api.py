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

        # Add first test bucket list
        url = reverse("bucketlist-list")
        self.bucketlist = {"title": "The List of Awesome",
                           "description": "Awesome things!",
                           "created_by": 1}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.get_token())
        response = self.client.post(url, data=self.bucketlist)
        self.first_bucketlist_id = str(response.data["id"])

        # Add second test bucket list
        self.bucketlist = {"title": "Knowledge Goals",
                           "description": "Things to learn",
                           "created_by": 1}
        response = self.client.post(url, data=self.bucketlist)
        self.second_bucketlist_id = str(response.data["id"])


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
        """ Test that user can add a bucket list """
        url = reverse("bucketlist-list")
        self.bucketlist = {"title": "Adventure!",
                           "description": "Adventurous stuff",
                           "created_by": 1}
        response = self.client.post(url, data=self.bucketlist)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bucketlist.objects.count(), 3)
        self.assertTrue("Adventure!" in response.data["title"])
        self.assertTrue("Adventurous stuff" in response.data["description"])

    def test_delete_bucketlist(self):
        """ Test deletion of bucket lists """
        url = "/api/v1/bucketlists/" + self.first_bucketlist_id + "/"
        response = self.client.delete(url)
        # Only one bucket list remains
        self.assertEqual(Bucketlist.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_edit_bucketlist(self):
        """ Test editing of bucket lists """
        self.bucketlist = {"title": "Mission Multilinguist",
                           "description": "Languages to learn"}
        url = "/api/v1/bucketlists/" + self.first_bucketlist_id + "/"
        response = self.client.put(url, data=self.bucketlist)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("Mission Multilinguist" in response.data["title"])
        self.assertTrue("Languages to learn" in response.data["description"])

    def test_get_bucketlists(self):
        """ Test that all bucket lists are displayed """
        url = reverse("bucketlist-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        bucketlist1 = response.data[0]
        bucketlist2 = response.data[1]
        # Both bucket lists are displayed
        self.assertEqual(bucketlist1.get("title"), "The List of Awesome")
        self.assertEqual(bucketlist2.get("title"), "Knowledge Goals")

    def test_get_bucketlist(self):
        """ Test that specified bucket list is displayed """
        # Get first bucket list
        url = "/api/v1/bucketlists/" + self.first_bucketlist_id + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), "The List of Awesome")

        # Get second bucket list
        url = "/api/v1/bucketlists/" + self.second_bucketlist_id + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), "Knowledge Goals")

    def test_get_nonexistent_bucketlist(self):
        """
        Test that specifying a bucket list with invalid id
        will throw an error
        """
        url = "/api/v1/bucketlists/1234/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue("Not found" in response.data["detail"])

    def test_unauthorized_access(self):
        """
        Test that users cannot edit or delete another user's bucket lists
        """
        # Register a new user
        url = reverse("user-list")
        self.user = {"username": "testuser2",
                     "email": "testuser2@email.com",
                     "password": "testpassword"}
        self.client.post(url, data=self.user)

        # Log new user in and obtain their token
        url = reverse("login")
        self.user = {"username": "testuser2",
                     "password": "testpassword"}
        response = self.client.post(url, data=self.user)
        token = str(response.data.get("token"))

        # Cannot edit bucket list
        self.bucketlist = {"title": "Mission Multilinguist",
                           "description": "Languages to learn"}
        url = "/api/v1/bucketlists/" + self.first_bucketlist_id + "/"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.put(url, data=self.bucketlist)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue("You do not have permission to perform this action"
                        in response.data["detail"])

        # Cannot delete bucket list
        url = "/api/v1/bucketlists/" + self.first_bucketlist_id + "/"
        response = self.client.delete(url)
        # Number of bucket lists remains the same
        self.assertEqual(Bucketlist.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

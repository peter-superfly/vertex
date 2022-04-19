from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestFirstApi(APITestCase):
    """
    """

    def setUp(self):
        self.first_test = reverse("first_test")

    def test_first_test_api(self):
        """
        """
        response = self.client.get(self.first_test)
        # Check status code for success url.
        assert response.status_code == status.HTTP_200_OK

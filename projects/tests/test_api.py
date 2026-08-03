from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from projects.models import Project

User = get_user_model()


class ProjectAPITest(APITestCase):
    """
    Tests de l'API des projets.
    """

    def setUp(self):
        """
        Prépare les données de test.
        """
        self.user = User.objects.create_user(
            username="user@example.com",
            password="password123",
        )

        self.project = Project.objects.create(
            name="Projet API",
            description="Projet de test",
            owner=self.user,
        )
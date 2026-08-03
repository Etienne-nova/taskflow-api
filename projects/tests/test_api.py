from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from projects.models import Project
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
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

    def test_authenticated_user_can_list_projects(self):
        """
        Vérifie qu'un utilisateur authentifié peut récupérer
        la liste de ses projets.
        """
        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        response = self.client.get("/api/projects/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
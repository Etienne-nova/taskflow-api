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

    def test_unauthenticated_user_cannot_list_projects(self):
        """
        Vérifie qu'un utilisateur non authentifié
        ne peut pas consulter la liste des projets.
        """
        response = self.client.get("/api/projects/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_only_sees_own_projects(self):
        """
        Vérifie qu'un utilisateur ne voit que
        les projets dont il est propriétaire.
        """
        other_user = User.objects.create_user(
            username="other_user",
            password="password123",
        )

        Project.objects.create(
            name="Projet secret",
            description="Ne doit pas être visible",
            owner=other_user,
        )

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        response = self.client.get("/api/projects/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["name"],
            "Projet API",
        )

    def test_authenticated_user_can_create_project(self):
        """
        Vérifie qu'un utilisateur authentifié
        peut créer un projet.
        """
        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        data = {
            "name": "Nouveau projet",
            "description": "Projet créé par test",
        }

        response = self.client.post(
            "/api/projects/",
            data,
            format="json",
        )
    
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Project.objects.filter(owner=self.user).count(),
            2,
        )

        self.assertTrue(
            Project.objects.filter(
                owner=self.user,
                name="Nouveau projet",
            ).exists()
        )

    def test_unauthenticated_user_cannot_create_project(self):
        """
        Vérifie qu'un utilisateur non authentifié
        ne peut pas créer un projet.
        """
        data = {
            "name": "Projet interdit",
            "description": "Ne doit pas être créé",
        }

        response = self.client.post(
            "/api/projects/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertFalse(
            Project.objects.filter(
                name="Projet interdit"
            ).exists()
        )
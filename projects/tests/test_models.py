from django.contrib.auth import get_user_model
from django.test import TestCase

from projects.models import Project

User = get_user_model()


class ProjectModelTest(TestCase):
    """
    Tests unitaires du modèle Project.
    """

    def test_project_string_representation(self):
        """
        Vérifie que __str__ retourne le nom du projet.
        """
        user = User.objects.create_user(
            username="user@example.com",
            password="password123",
        )

        project = Project.objects.create(
            name="TaskFlow API",
            description="Projet de test",
            owner=user,
        )

        self.assertEqual(str(project), "TaskFlow API")
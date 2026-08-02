from rest_framework import viewsets

from .models import Project
from .serializers import ProjectSerializer
from core.permissions.project_permissions import IsProjectOwner
from django_filters.rest_framework import DjangoFilterBackend

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API CRUD des projets.
    """

    serializer_class = ProjectSerializer
    permission_classes = [IsProjectOwner]

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        "name",
        "created_at",
    ]

    def get_queryset(self):
        """
        Retourne uniquement les projets appartenant
        à l'utilisateur connecté.
        """
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Définit automatiquement le propriétaire
        lors de la création d'un projet.
        """
        serializer.save(owner=self.request.user)
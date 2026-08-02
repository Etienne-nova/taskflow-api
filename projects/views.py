from rest_framework import viewsets

from .models import Project
from .serializers import ProjectSerializer
from core.permissions.project_permissions import IsProjectOwner
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API CRUD des projets.
    """

    serializer_class = ProjectSerializer
    permission_classes = [IsProjectOwner]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "name",
        "created_at",
    ]
    
    search_fields = [
        "name",
        "description",
    ]

    def get_queryset(self):
        """
        Retourne uniquement les projets appartenant
        à l'utilisateur connecté en optimisant
        les relations avec la base de données.
        """
        return (
            Project.objects
            .filter(owner=self.request.user)
            .select_related("owner")
            .prefetch_related("members")
        )
    
    def perform_create(self, serializer):
        """
        Définit automatiquement le propriétaire
        lors de la création d'un projet.
        """
        serializer.save(owner=self.request.user)
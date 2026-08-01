from rest_framework import viewsets

from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API CRUD des projets.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
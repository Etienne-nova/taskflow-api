from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer du modèle Task.
    """

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "project",
            "assigned_to",
            "status",
            "due_date",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

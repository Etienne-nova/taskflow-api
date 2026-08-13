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

    def validate(self, attrs):
        """
        Vérifie qu'un utilisateur assigné est membre du projet.
        """
        project = attrs.get("project")

        if project is None and self.instance is not None:
            project = self.instance.project

        assigned_to = attrs.get("assigned_to")

        if assigned_to is not None and project is not None:
            if not project.members.filter(pk=assigned_to.pk).exists():
                raise serializers.ValidationError(
                    {
                        "assigned_to": (
                            "L'utilisateur assigné doit être membre du projet."
                        )
                    }
                )

        return attrs

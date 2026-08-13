from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from projects.models import Project
from tasks.models import Task


class Command(BaseCommand):
    help = "Crée un jeu de données de démonstration."

    def handle(self, *args, **options):
        User = get_user_model()

        user, _ = User.objects.get_or_create(
            username="demo",
            defaults={
                "email": "demo@example.com",
            },
        )

        if not user.has_usable_password():
            user.set_password("demo1234")
            user.save()

        project, _ = Project.objects.get_or_create(
            name="Projet Démo",
            defaults={
                "description": "Projet généré automatiquement.",
                "owner": user,
            },
        )

        project.members.add(user)

        tasks = [
            (
                "Créer l'API",
                Task.Status.TODO,
            ),
            (
                "Écrire les tests",
                Task.Status.IN_PROGRESS,
            ),
            (
                "Déployer l'application",
                Task.Status.DONE,
            ),
        ]

        created = 0

        for title, status in tasks:
            _, was_created = Task.objects.get_or_create(
                project=project,
                title=title,
                defaults={
                    "description": f"Tâche : {title}",
                    "status": status,
                    "assigned_to": user,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Données de démonstration prêtes ({created} tâche(s) créée(s))."
            )
        )

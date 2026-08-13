from celery import shared_task


@shared_task
def notify_task_assignment(task_id, user_id):
    """
    Tâche asynchrone exécutée lors de l'assignation d'une tâche.
    """
    print(f"Tâche {task_id} assignée à l'utilisateur {user_id}")
    return {
        "task_id": task_id,
        "user_id": user_id,
    }

from celery import shared_task
from core.celery import app
from todo.models import Task


@shared_task()
def clean_complete_task():
    complete_tasks = Task.objects.filter(complete=True)
    if complete_tasks:
        c = len(complete_tasks)
        complete_tasks .delete()
        print(f'{c} completed Tasks deleted!')
    else:
        print(f'No completed tasks found!')

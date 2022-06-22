from celery import Task, shared_task


@shared_task(bound=True)
def fetch_examples(task: Task, word_id: int) -> None:
    pass

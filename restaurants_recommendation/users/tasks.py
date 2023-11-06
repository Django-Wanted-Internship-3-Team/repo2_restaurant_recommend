from celery import shared_task


@shared_task
def demo():
    return "demo"

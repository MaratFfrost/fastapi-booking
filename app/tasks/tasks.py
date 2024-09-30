from app.tasks.celery import celery

@celery.tasks
def name():
  pass

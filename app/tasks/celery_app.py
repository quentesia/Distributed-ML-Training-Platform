from celery import Celery
from app.config import settings

# Create Celery app
celery_app = Celery(
    "ml_training_pipeline",
    broker=settings.rabbitmq_url,
    backend=settings.redis_url,
    include=['app.tasks.training'] 
)

# Celery configuration
celery_app.conf.update(
    # Task settings
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    
    # Worker settings
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    
    # Result settings
    result_expires=3600,  
)
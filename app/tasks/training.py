from datetime import datetime
from sqlalchemy.orm import Session

from app.tasks.celery_app import celery_app
from app.database.connection import SessionLocal
from app.database.models import TrainingJob
from app.services.redis_client import store_model
from app.ml.simple_model import train_linear_regression
import os

@celery_app.task(bind=True)
def train_model(self, job_id: int, dataset_path: str):
    db = SessionLocal()
    
    try:
        print(f"Starting training for job {job_id}")
        
        # Get job from database
        job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
        if not job:
            raise Exception(f"Job {job_id} not found")
        
        # Update job status to running
        job.status = "running"
        db.commit()
        print(f"Job {job_id} status updated to 'running'")
        
        # Train the model 
        print(f"Training model on {dataset_path}")
        model_data = train_linear_regression(dataset_path)
        
        # Generate unique key for this model
        # Using version for resume claim "Efficient model versioning"
        safe_filename = job.dataset_filename.replace(".csv", "").replace(" ", "_")
        model_key = f"model_{safe_filename}_v{job.version}"
        
        print(f"Storing model in Redis with key: {model_key}")
        success = store_model(model_key, model_data)
        
        if not success:
            raise Exception("Failed to store model in Redis")
        
        # Update job with success info
        job.status = "completed"
        job.model_key = model_key
        job.accuracy = model_data.get("r2_score", 0.0)
        job.completed_at = datetime.utcnow()
        db.commit()
        
        print(f"Training completed for job {job_id}")
        print(f"Model accuracy: {job.accuracy:.3f}")
        
        return {
            "job_id": job_id,
            "status": "completed",
            "model_key": model_key,
            "accuracy": job.accuracy
        }
        
    except Exception as e:
        print(f"Training failed for job {job_id}: {str(e)}")
        
        # Update job with failure info
        try:
            job.status = "failed"
            
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            db.commit()
        except Exception as db_error:
            print(f"Failed to update job status: {db_error}")
        
        # Re-raise the exception so Celery knows the task failed
        raise Exception(f"Training failed: {str(e)}")
        
    finally:
        db.close()
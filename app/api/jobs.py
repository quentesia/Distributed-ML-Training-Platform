import os
from typing import Any, Dict
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import TrainingJob

router = APIRouter(prefix="/jobs", tags=["Training Jobs"])


@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...), db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Upload a CSV file and queue it for ML model training

    Args:
        file: CSV file upload
        db: Database session

    Returns:
        Job information with job_id for tracking
    """

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    file_size = 0
    file_content = await file.read()
    file_size = len(file_content)

    if file_size > 10 * 1024**2:
        raise HTTPException(
            status_code=400, detail="Only files under 10 MB are accepted currently."
        )

    os.makedirs("uploads", exist_ok=True)

    tmp_filename = f"{uuid4()}_{file.filename}"
    file_path = f"uploads/{tmp_filename}"

    with open(file_path, "wb") as f:
        f.write(file_content)

    job = TrainingJob(dataset_filename=file.filename, status="pending")

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "status": job.status,
        "dataset_filename": job.dataset_filename,
        "message": "Dataset uploaded successfully. Training will begin shortly.",
    }

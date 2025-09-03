from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from app.database.connection import Base


class TrainingJob(Base):
    __tablename__ = "training_jobs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(
        String, default="pending"
    )  # can be pending, running, completed or failed
    dataset_filename = Column(String, nullable=False)
    model_key = Column(String, nullable=True)
    accuracy = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    version = Column(Integer, default=1)

    def __repr__(self):
        return f"<TrainingJob(id={self.id}, status={self.status})>"

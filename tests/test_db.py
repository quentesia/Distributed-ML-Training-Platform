from app.database.connection import Base, SessionLocal, engine
from app.database.models import TrainingJob

print("Initializing test database tables")
Base.metadata.create_all(bind=engine)

print("connecting to database")
db = SessionLocal()

try:
    print("Creating a test job")
    test_job = TrainingJob(dataset_filename="test_data.csv", status="pending")
    db.add(test_job)
    db.commit()

    print("Queying the commited job")
    job = db.query(TrainingJob).first()

    assert job.dataset_filename == "test_data.csv"
    assert job.status == "pending"
finally:
    db.close()

print("Database connection is working as expected")

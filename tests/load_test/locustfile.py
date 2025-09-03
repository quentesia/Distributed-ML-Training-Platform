import random
from locust import HttpUser, task, between

class MLPlatformUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        # Create a dummy CSV content for valid uploads
        self.csv_content = "feature1,feature2,target\n1,2,3\n4,5,6"

    @task
    def upload_dataset(self):
        # Generate a unique filename to avoid version conflicts in this test
        filename = f"dataset_{random.randint(1, 100000)}.csv"
        
        files = {
            "file": (filename, self.csv_content, "text/csv")
        }
        
        with self.client.post("/jobs/upload", files=files, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}: {response.text}")

if __name__ == "__main__":
    import os
    os.system("locust -f tests/load_test/locustfile.py")

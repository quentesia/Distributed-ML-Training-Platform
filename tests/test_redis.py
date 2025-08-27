import numpy as np
from sklearn.linear_model import LinearRegression

from app.services.redis_client import delete_model, get_model, list_models, store_model

X = np.array([[1, 2], [2, 4], [3, 6], [4, 8]])
y = np.array([3, 6, 9, 12])

model = LinearRegression()
model.fit(X, y)

test_features = ["feature1", "feature2"]
test_accuracy = 0.95

# Package model with metadata
model_data = {
    "model": model,
    "feature_names": test_features,
    "accuracy": test_accuracy,
}

# Test storing model
print("Attempting to store model in Redis...")
success = store_model("test_model", model_data)

if success:
    print("Redis store succesful")
else:
    print("Failed to store on redis")


# Test retrieving model
print("Retrieving model from Redis...")
retrieved_data = get_model("test_model")

if retrieved_data:
    print(f"Retrieved data: {retrieved_data}")
    assert retrieved_data["accuracy"] == test_accuracy
    assert retrieved_data["feature_names"] == test_features

    # Test the model still works
    test_prediction = retrieved_data["model"].predict([[5, 10]])
    print(f"Test prediction: {test_prediction[0]}")
else:
    print("❌ Failed to retrieve model")

# Test listing models
print(f"\nAll models in Redis: {list_models()}")

# Clean up
print("\nCleaning up...")
delete_result = delete_model("test_model")

if delete_result:
    print("Redis store succesful")
else:
    print("Failed to store on redis")

print(f"Models after cleanup: {list_models()}")

import os

import pandas as pd

from app.ml.simple_model import make_prediction, train_linear_regression

"""Test the ML training with sample data"""

print("Creating sample training data...")

# Create sample sales prediction data
sample_data = pd.DataFrame(
    {
        "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "advertising": [100, 150, 200, 120, 180, 220, 160, 190, 210, 170, 240, 130],
        "sales": [
            1000,
            1200,
            1500,
            1100,
            1350,
            1600,
            1250,
            1400,
            1550,
            1300,
            1700,
            1150,
        ],
    }
)

# Save to CSV file
test_file = "test_sample_data.csv"
sample_data.to_csv(test_file, index=False)
print(f"✅ Created test CSV: {test_file}")

try:
    print("\nTraining linear regression model...")

    # Train model
    model_data = train_linear_regression(test_file)
    print(" Successfully trained the model.")

    print("Testing its predictions:")
    test_cases = [
        ([1, 100], "month=1, advertising=100", 963.11),
        ([6, 200], "month=6, advertising=200", 1479.23),
        ([12, 150], "month=12, advertising=150", 1236.73),
    ]

    for features, description, expected_value in test_cases:
        result = make_prediction(model_data, features)
        print(f"{description} → ${result['prediction']:.2f}")

        # You can add specific assertions here after seeing the values
        assert abs(result["prediction"] - expected_value) < 0.01
        print(f"Assertion passed for {description}")

except Exception as e:
    print(f"Test failed -> {e}")
finally:
    if os.path.exists(test_file):
        os.remove(test_file)

from typing import Any, Dict

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def train_linear_regression(csv_path: str) -> Dict[str, Any]:
    try:
        df = pd.read_csv(csv_path)

        if df.empty:
            raise ValueError("The CSV file specified is empyty")

        if len(df.columns) < 2:
            raise ValueError(
                "CSV must have at least 2 columns to be parsed i.e. Feature and Target"
            )

        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        # Check for non-numeric data
        if not all(X.dtypes.apply(lambda x: np.issubdtype(x, np.number))):
            raise ValueError("All feature columns must be numeric")

        if not np.issubdtype(y.dtype, np.number):
            raise ValueError("Target column must be numeric")

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Create model package with metadata
        model_data = {
            "model": model,
            "feature_names": list(X.columns),
            "target_name": y.name if hasattr(y, "name") else "target",
            "n_features": len(X.columns),
            "n_samples": len(df),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "mse": float(mse),
            "r2_score": float(r2),
            "model_type": "LinearRegression",
        }

        return model_data

    except Exception as e:
        raise Exception(f"Training failed: {str(e)}")


def make_prediction(model_data: Dict[str, Any], features: list) -> Dict[str, Any]:
    try:
        model = model_data["model"]

        # Validate input
        if len(features) != model_data["n_features"]:
            raise ValueError(
                f"Expected {model_data['n_features']} features, got {len(features)}"
            )

        X = np.array(features).reshape(1, -1)

        # Make prediction
        prediction = model.predict(X)[0]

        return {
            "prediction": float(prediction),
            "features_used": features,
            "feature_names": model_data["feature_names"],
            "model_type": model_data["model_type"],
        }

    except Exception as e:
        raise Exception(f"Prediction failed: {str(e)}")

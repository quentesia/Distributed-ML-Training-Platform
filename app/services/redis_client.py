import pickle
from typing import Any, Optional

import redis

from app.config import settings

redis_client = redis.from_url(settings.redis_url)


def store_model(model_key: str, model_data: Any) -> bool:
    try:
        serialized_model = pickle.dumps(model_data)
        redis_client.set(model_key, serialized_model)

        return True

    except Exception:
        print(
            f"Error while trying to serialize and store model '{model_key}' in redis."
        )
        return False


def get_model(model_key: str) -> Optional[Any]:
    try:
        return pickle.loads(model) if (model := redis_client.get(model_key)) else None
    except Exception:
        print(f"Error while trying to retrieve model '{model_key}' from redis.")
        return None


def delete_model(model_key: str) -> bool:
    """
    Delete a model from Redis

    """
    try:
        result = redis_client.delete(model_key)
        return result > 0  # Redis returns number of keys deleted
    except Exception as e:
        print(f"Error deleting model {model_key}: {e}")
        return False


def list_models() -> list:
    """
    List all model keys in Redis

    Returns:
        List of model keys
    """
    try:
        keys = redis_client.keys("model_*")
        return [key.decode("utf-8") for key in keys]
    except Exception as e:
        print(f"Error listing models: {e}")
        return []

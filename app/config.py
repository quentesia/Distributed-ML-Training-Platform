from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://quentesia:postgres@localhost:5432/mlpipeline"
    redis_url: str = "redis://localhost:6379"
    rabbitmq_url: str = "amqp://admin:admin@localhost:5672"

    app_name: str = "ML Training Pipeline"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()

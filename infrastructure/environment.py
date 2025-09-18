from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseSettings):
    uri: str
    db: str

    model_config = SettingsConfigDict(env_prefix="mongo_", extra="ignore")


class RedisSettings(BaseSettings):
    uri: str

    model_config = SettingsConfigDict(env_prefix="redis_", extra="ignore")


class Environment(BaseSettings):
    mongodb: MongoSettings = MongoSettings()
    redis: RedisSettings = RedisSettings()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


env: Environment = Environment()

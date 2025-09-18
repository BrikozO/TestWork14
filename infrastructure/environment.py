from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseSettings):
    uri: str
    db: str

    model_config = SettingsConfigDict(env_prefix="mongo_", extra="ignore")


class Environment(BaseSettings):
    mongodb: MongoSettings = MongoSettings()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


env: Environment = Environment()

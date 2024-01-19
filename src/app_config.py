from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    OC_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


app_config = AppConfig()
